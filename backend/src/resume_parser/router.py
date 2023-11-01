from typing import Annotated

from fastapi import APIRouter, status, UploadFile, Form

from src.resume_parser.service import process_files


router = APIRouter()


@router.post("/process", status_code=status.HTTP_200_OK)
async def parser(
    files: list[UploadFile],
    job_description: Annotated[str, Form()] = "",
    job_title: Annotated[str, Form()] = "",
):
    result = await process_files(files, job_description, job_title)
    return result
