# generated by datamodel-codegen:
#   filename:  aqt_public.yml

from __future__ import annotations

from enum import Enum
from typing import Annotated, Dict, List, Literal, Optional, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, RootModel


class GateR(BaseModel):
    """
    A single-qubit rotation.

    Describes a rotation of angle θ around axis φ in the equatorial plane of the Bloch sphere.

    Angles are expressed in units of π.
    """

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )
    operation: Annotated[Literal["R"], Field("R", title="Operation")]
    phi: Annotated[float, Field(ge=0.0, le=2.0, title="Phi")]
    qubit: Annotated[int, Field(ge=0, title="Qubit")]
    theta: Annotated[float, Field(ge=0.0, le=1.0, title="Theta")]


class Qubit(RootModel[int]):
    model_config = ConfigDict(
        frozen=True,
    )
    root: Annotated[int, Field(ge=0)]


class GateRXX(BaseModel):
    """
    A parametric 2-qubits X⊗X gate with angle θ.

    The angle is expressed in units of π. The gate is maximally entangling
    for θ=0.5 (π/2).
    """

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )
    operation: Annotated[Literal["RXX"], Field("RXX", title="Operation")]
    qubits: Annotated[List[Qubit], Field(max_length=2, min_length=2, title="Qubits")]
    theta: Annotated[float, Field(ge=0.0, le=0.5, title="Theta")]


class GateRZ(BaseModel):
    """
    A single-qubit rotation of angle φ around the Z axis of the Bloch sphere.
    """

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )
    operation: Annotated[Literal["RZ"], Field("RZ", title="Operation")]
    phi: Annotated[float, Field(title="Phi")]
    qubit: Annotated[int, Field(ge=0, title="Qubit")]


class JobUser(BaseModel):
    model_config = ConfigDict(
        frozen=True,
    )
    job_id: Annotated[UUID, Field(title="Job Id")]
    """
    Id that uniquely identifies the job. This is used to request results.
    """
    job_type: Annotated[
        Literal["quantum_circuit"], Field("quantum_circuit", title="Job Type")
    ]
    label: Annotated[Optional[str], Field(None, title="Label")]
    resource_id: Annotated[str, Field("", title="Resource Id")]
    workspace_id: Annotated[str, Field("", title="Workspace Id")]


class Measure(BaseModel):
    """
    Measurement operation.

    The MEASURE operation instructs the resource
    to perform a projective measurement of all qubits.
    """

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )
    operation: Annotated[Literal["MEASURE"], Field("MEASURE", title="Operation")]


class OperationModel(RootModel[Union[GateRZ, GateR, GateRXX, Measure]]):
    model_config = ConfigDict(
        frozen=True,
    )
    root: Annotated[
        Union[GateRZ, GateR, GateRXX, Measure],
        Field(discriminator="operation", title="OperationModel"),
    ]
    """
    Model for the items in a Circuit.

    This extra wrapper is introduced to leverage the pydantic
    tagged-union parser.
    """


class RRCancelled(BaseModel):
    model_config = ConfigDict(
        frozen=True,
    )
    status: Annotated[Literal["cancelled"], Field("cancelled", title="Status")]


class RRError(BaseModel):
    model_config = ConfigDict(
        frozen=True,
    )
    message: Annotated[str, Field(title="Message")]
    status: Annotated[Literal["error"], Field("error", title="Status")]


class ResultItem(RootModel[int]):
    model_config = ConfigDict(
        frozen=True,
    )
    root: Annotated[int, Field(ge=0, le=1)]


class RRFinished(BaseModel):
    """
    Contains the measurement data of a finished circuit.
    """

    model_config = ConfigDict(
        frozen=True,
    )
    result: Annotated[Dict[str, List[List[ResultItem]]], Field(title="Result")]
    status: Annotated[Literal["finished"], Field("finished", title="Status")]


class RROngoing(BaseModel):
    model_config = ConfigDict(
        frozen=True,
    )
    finished_count: Annotated[int, Field(ge=0, title="Finished Count")]
    status: Annotated[Literal["ongoing"], Field("ongoing", title="Status")]


class RRQueued(BaseModel):
    model_config = ConfigDict(
        frozen=True,
    )
    status: Annotated[Literal["queued"], Field("queued", title="Status")]


class Type(Enum):
    simulator = "simulator"
    device = "device"


class Resource(BaseModel):
    model_config = ConfigDict(
        frozen=True,
    )
    id: Annotated[str, Field(title="Id")]
    name: Annotated[str, Field(title="Name")]
    type: Annotated[Type, Field(title="Type")]


class UnknownJob(BaseModel):
    model_config = ConfigDict(
        frozen=True,
    )
    job_id: Annotated[UUID, Field(title="Job Id")]
    message: Annotated[
        Literal["unknown job_id"], Field("unknown job_id", title="Message")
    ]


class ValidationError(BaseModel):
    model_config = ConfigDict(
        frozen=True,
    )
    loc: Annotated[List[Union[str, int]], Field(title="Location")]
    msg: Annotated[str, Field(title="Message")]
    type: Annotated[str, Field(title="Error Type")]


class Workspace(BaseModel):
    model_config = ConfigDict(
        frozen=True,
    )
    id: Annotated[str, Field(title="Id")]
    resources: Annotated[List[Resource], Field(title="Resources")]


class Circuit(RootModel[List[OperationModel]]):
    """
    Json encoding of a quantum circuit.
    """

    model_config = ConfigDict(
        frozen=True,
    )
    root: Annotated[
        List[OperationModel],
        Field(
            examples=[[
                {"operation": "RZ", "phi": 0.5, "qubit": 0},
                {"operation": "R", "phi": 0.25, "qubit": 1, "theta": 0.5},
                {"operation": "RXX", "qubits": [0, 1], "theta": 0.5},
                {"operation": "MEASURE"},
            ]],
            max_length=10000,
            min_length=1,
            title="Circuit",
        ),
    ]
    """
    Json encoding of a quantum circuit.
    """


class HTTPValidationError(BaseModel):
    model_config = ConfigDict(
        frozen=True,
    )
    detail: Annotated[Optional[List[ValidationError]], Field(None, title="Detail")]


class JobResponseRRCancelled(BaseModel):
    model_config = ConfigDict(
        frozen=True,
    )
    job: JobUser
    response: RRCancelled


class JobResponseRRError(BaseModel):
    model_config = ConfigDict(
        frozen=True,
    )
    job: JobUser
    response: RRError


class JobResponseRRFinished(BaseModel):
    model_config = ConfigDict(
        frozen=True,
    )
    job: JobUser
    response: RRFinished


class JobResponseRROngoing(BaseModel):
    model_config = ConfigDict(
        frozen=True,
    )
    job: JobUser
    response: RROngoing


class JobResponseRRQueued(BaseModel):
    model_config = ConfigDict(
        frozen=True,
    )
    job: JobUser
    response: RRQueued


class QuantumCircuit(BaseModel):
    """
    A quantum circuit-type job that can run on a computing resource.
    """

    model_config = ConfigDict(
        frozen=True,
    )
    number_of_qubits: Annotated[int, Field(gt=0, title="Number Of Qubits")]
    quantum_circuit: Circuit
    repetitions: Annotated[int, Field(gt=0, title="Repetitions")]


class QuantumCircuits(BaseModel):
    """
    A collection of quantum circuits representing a single job.
    """

    model_config = ConfigDict(
        frozen=True,
    )
    circuits: Annotated[List[QuantumCircuit], Field(min_length=1, title="Circuits")]


class ResultResponse(
    RootModel[
        Union[
            JobResponseRRQueued,
            JobResponseRROngoing,
            JobResponseRRFinished,
            JobResponseRRError,
            JobResponseRRCancelled,
            UnknownJob,
        ]
    ]
):
    model_config = ConfigDict(
        frozen=True,
    )
    root: Annotated[
        Union[
            JobResponseRRQueued,
            JobResponseRROngoing,
            JobResponseRRFinished,
            JobResponseRRError,
            JobResponseRRCancelled,
            UnknownJob,
        ],
        Field(
            examples=[
                {
                    "description": (
                        "Job waiting in the queue to be picked up by the Quantum"
                        " computer"
                    ),
                    "summary": "Queued Job",
                    "value": {
                        "job": {
                            "job_id": "ccaa39de-d0f3-4c8b-bdb1-4d74f0c2f450",
                            "job_type": "quantum_circuit",
                            "label": "Example computation",
                            "payload": {
                                "circuits": [{
                                    "number_of_qubits": 2,
                                    "quantum_circuit": [
                                        {"operation": "RZ", "phi": 0.5, "qubit": 0},
                                        {
                                            "operation": "R",
                                            "phi": 0.25,
                                            "qubit": 1,
                                            "theta": 0.5,
                                        },
                                        {
                                            "operation": "RXX",
                                            "qubits": [0, 1],
                                            "theta": 0.5,
                                        },
                                        {"operation": "MEASURE"},
                                    ],
                                    "repetitions": 5,
                                }]
                            },
                        },
                        "response": {"status": "queued"},
                    },
                },
                {
                    "description": (
                        "Job that is currently being processed by the Quantum computer"
                    ),
                    "summary": "Ongoing Job",
                    "value": {
                        "job": {
                            "job_id": "ccaa39de-d0f3-4c8b-bdb1-4d74f0c2f450",
                            "job_type": "quantum_circuit",
                            "label": "Example computation",
                            "payload": {
                                "circuits": [{
                                    "number_of_qubits": 2,
                                    "quantum_circuit": [
                                        {"operation": "RZ", "phi": 0.5, "qubit": 0},
                                        {
                                            "operation": "R",
                                            "phi": 0.25,
                                            "qubit": 1,
                                            "theta": 0.5,
                                        },
                                        {
                                            "operation": "RXX",
                                            "qubits": [0, 1],
                                            "theta": 0.5,
                                        },
                                        {"operation": "MEASURE"},
                                    ],
                                    "repetitions": 5,
                                }]
                            },
                        },
                        "response": {"finished_count": 0, "status": "ongoing"},
                    },
                },
                {
                    "description": (
                        "Job that created an error while being processed by the Quantum"
                        " computer"
                    ),
                    "summary": "Failed Job",
                    "value": {
                        "job": {
                            "job_id": "ccaa39de-d0f3-4c8b-bdb1-4d74f0c2f450",
                            "job_type": "quantum_circuit",
                            "label": "Example computation",
                            "payload": {
                                "circuits": [{
                                    "number_of_qubits": 2,
                                    "quantum_circuit": [
                                        {"operation": "RZ", "phi": 0.5, "qubit": 0},
                                        {
                                            "operation": "R",
                                            "phi": 0.25,
                                            "qubit": 1,
                                            "theta": 0.5,
                                        },
                                        {
                                            "operation": "RXX",
                                            "qubits": [0, 1],
                                            "theta": 0.5,
                                        },
                                        {"operation": "MEASURE"},
                                    ],
                                    "repetitions": 5,
                                }]
                            },
                        },
                        "response": {
                            "message": "detailed error message",
                            "status": "error",
                        },
                    },
                },
                {
                    "description": (
                        "Job that has been cancelled by the user, before it could be"
                        " processed by the Quantum computer"
                    ),
                    "summary": "Cancelled Job",
                    "value": {
                        "job": {
                            "job_id": "ccaa39de-d0f3-4c8b-bdb1-4d74f0c2f450",
                            "job_type": "quantum_circuit",
                            "label": "Example computation",
                            "payload": {
                                "circuits": [{
                                    "number_of_qubits": 2,
                                    "quantum_circuit": [
                                        {"operation": "RZ", "phi": 0.5, "qubit": 0},
                                        {
                                            "operation": "R",
                                            "phi": 0.25,
                                            "qubit": 1,
                                            "theta": 0.5,
                                        },
                                        {
                                            "operation": "RXX",
                                            "qubits": [0, 1],
                                            "theta": 0.5,
                                        },
                                        {"operation": "MEASURE"},
                                    ],
                                    "repetitions": 5,
                                }]
                            },
                        },
                        "response": {"status": "cancelled"},
                    },
                },
                {
                    "description": (
                        "Job that has been successfully processed by a quantum computer"
                        " or simulator"
                    ),
                    "summary": "Finished Job",
                    "value": {
                        "job": {
                            "job_id": "ccaa39de-d0f3-4c8b-bdb1-4d74f0c2f450",
                            "job_type": "quantum_circuit",
                            "label": "Example computation",
                            "payload": {
                                "circuits": [{
                                    "number_of_qubits": 2,
                                    "quantum_circuit": [
                                        {"operation": "RZ", "phi": 0.5, "qubit": 0},
                                        {
                                            "operation": "R",
                                            "phi": 0.25,
                                            "qubit": 1,
                                            "theta": 0.5,
                                        },
                                        {
                                            "operation": "RXX",
                                            "qubits": [0, 1],
                                            "theta": 0.5,
                                        },
                                        {"operation": "MEASURE"},
                                    ],
                                    "repetitions": 5,
                                }]
                            },
                        },
                        "response": {
                            "result": {"0": [[1, 0], [1, 1], [0, 0], [1, 1], [1, 1]]},
                            "status": "finished",
                        },
                    },
                },
                {
                    "description": "The supplied job id could not be found",
                    "summary": "Unknown Job",
                    "value": {
                        "job_id": "3aa8b827-4ff0-4a36-b1a6-f9ff6dee59ce",
                        "message": "unknown job_id",
                    },
                },
            ],
            title="ResultResponse",
        ),
    ]


class JobSubmission(BaseModel):
    model_config = ConfigDict(
        frozen=True,
    )
    job_type: Annotated[
        Literal["quantum_circuit"], Field("quantum_circuit", title="Job Type")
    ]
    label: Annotated[Optional[str], Field(None, title="Label")]
    payload: QuantumCircuits
