from typing import List, Type

import pytest

from konan_sdk.endpoints.base_endpoint import KonanBaseEndpoint
from konan_sdk.endpoints.interfaces import KonanEndpointRequest, KonanEndpointResponse
from konan_sdk.endpoints.konan_endpoints import FeedbackEndpoint
from konan_sdk.konan_types import KonanFeedbackStatus, KonanFeedbackSubmission, KonanFeedbacksResult

from tests.endpoints.test_endpoint import EndpointCommonTests


class TestFeedbackEndpoint(EndpointCommonTests):
    @property
    def _endpoint_class(self) -> Type[KonanBaseEndpoint]:
        return FeedbackEndpoint

    def test_prepare_request(self):
        feedbacks_dict = [
            {
                'prediction_uuid': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
                'target': {
                    'prediction': 0.9,
                },
            },
            {
                'prediction_uuid': '423101a4-d0e4-44a1-bc5d-52157d363ab9',
                'target': {
                    'prediction': 0.85,
                },
            },
        ]
        konan_endpoint_request = self.endpoint.prepare_request(
            [
                KonanFeedbackSubmission(
                    feedback_dict['prediction_uuid'],
                    feedback_dict['target'],
                )
                for feedback_dict in feedbacks_dict
            ]
        )

        assert isinstance(konan_endpoint_request, KonanEndpointRequest)
        assert konan_endpoint_request.params is None
        assert isinstance(konan_endpoint_request.json, dict)
        assert konan_endpoint_request.json == {
            'feedback': feedbacks_dict,
        }

    @pytest.mark.parametrize(
        argnames=['feedbacks_data', 'success_num', 'failure_num'],
        argvalues=[
            (
                [
                    {
                        'message': 'success',
                        'prediction_uuid': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
                        'status': 201,
                    },
                    {
                        'message': 'success',
                        'prediction_uuid': '423101a4-d0e4-44a1-bc5d-52157d363ab9',
                        'status': 201,
                    },
                ], 2, 0
            ),
            (
                [], 0, 0,
            ),
            (
                [
                    {
                        'message': 'failure',
                        'prediction_uuid': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
                        'status': 404,
                    },
                    {
                        'message': 'failure',
                        'prediction_uuid': '423101a4-d0e4-44a1-bc5d-52157d363ab9',
                        'status': 409,
                    },
                ], 0, 2
            ),
        ],
        ids=[
            '2 success - 0 failure',
            '0 success - 0 failure',
            '0 success - 2 failure',
        ],
    )
    def test_process_response(self, feedbacks_data, success_num, failure_num):
        expected_feedbacks_status = [
            KonanFeedbackStatus(
                feedback_data['prediction_uuid'],
                feedback_data['status'],
                feedback_data['message'],
            )
            for feedback_data in feedbacks_data
        ]

        konan_feedback_result: KonanFeedbacksResult = self.endpoint.process_response(
            KonanEndpointResponse(
                status_code=207,
                json={
                    'data': feedbacks_data,
                    'success': success_num,
                    'failure': failure_num,
                    'total': success_num + failure_num,
                },
            )
        )

        assert isinstance(konan_feedback_result, KonanFeedbacksResult)
        assert konan_feedback_result.success_count == success_num
        assert konan_feedback_result.failure_count == failure_num
        assert konan_feedback_result.total_count == success_num + failure_num
        assert isinstance(konan_feedback_result.feedbacks_status, List)
        assert all(
            [
                isinstance(feedback_status, KonanFeedbackStatus)
                for feedback_status in konan_feedback_result.feedbacks_status
            ]
        )
        assert len(konan_feedback_result.feedbacks_status) == len(expected_feedbacks_status)
        assert set(konan_feedback_result.feedbacks_status) == set(expected_feedbacks_status)
