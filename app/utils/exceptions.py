from fastapi import HTTPException, status


class BaseException_(HTTPException):
    def istype(self, exp: "BaseException_") -> bool:
        return self.status_code == exp.status_code and self.detail == exp.detail


class _TemplateException(BaseException_):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


DuplicateValue = _TemplateException(
    detail="Duplicate Value",
    status_code=status.HTTP_409_CONFLICT,
)
NotFound = _TemplateException(
    detail="Entity Not Found",
    status_code=status.HTTP_404_NOT_FOUND,
)
ServerError = _TemplateException(
    detail="Internal Server Error",
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
)
NonOwnerAccessForbidden = _TemplateException(
    detail="Access to ad is forbidden because you are not the owner",
    status_code=status.HTTP_403_FORBIDDEN,
)
