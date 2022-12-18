
from typing import Generator, Generic, List, Optional, TypeVar

from konan_sdk.auth import _AbstractKonanAuth
from konan_sdk.endpoints.base_endpoint import KonanEndpointOperationEnum
from konan_sdk.endpoints.interfaces import KonanEndpointRequest, KonanEndpointResponse

ReqT = TypeVar('ReqT')
ResT = TypeVar('ResT')


class KonanPaginatedEndpointMixin(Generic[ReqT, ResT]):
    def __init__(self, *args, auth_object: Optional[_AbstractKonanAuth], **kwargs) -> None:
        # self._count: Optional[int] = None
        self._next_url: Optional[str] = None
        self._auth_object: Optional[_AbstractKonanAuth] = auth_object
        # self._previous_url: Optional[str] = None

        super().__init__(*args, **kwargs)

    @property
    def endpoint_operation(self) -> KonanEndpointOperationEnum:
        return KonanEndpointOperationEnum.GET

    @property
    def request_url(self) -> str:
        return self._next_url or super().request_url

    def process_response(self, endpoint_response: KonanEndpointResponse) -> List[ResT]:
        # self._count = endpoint_response.json.get('count')
        self._next_url = endpoint_response.json.get('next')
        # self._previous_url = endpoint_response.json.get('previous')

        results: List[ResT] = self._process_page(results=endpoint_response.json.get('results', []))
        return results

    def prepare_request(self, request_object: ReqT) -> KonanEndpointRequest:
        # NOTE When using a paginated endpoint, `konan-backend` gives us the `next_page` URL which already includes the
        # the query parameters in it.
        #
        # As such, need to override the prepare_request() method to remove the `params`,
        # but not for the "initial" hit on the endpoint.
        endpoint_request: KonanEndpointRequest = super().prepare_request(request_object=request_object)
        if self._next_url is not None:
            endpoint_request.params = None
        return endpoint_request

    def get_pages(self, request_object: ReqT) -> Generator[List[ResT], None, None]:
        # TODO: refactor prepare_request to allow to dynamically set page_size
        first_page: List[ResT] = self.request(request_object=request_object)
        yield first_page
        while self._next_url is not None:
            if self._auth_object is not None:
                self._auth_object.auto_refresh_token()
            next_page: List[ResT] = self.request(request_object=request_object)
            yield next_page
