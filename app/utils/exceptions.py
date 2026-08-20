from fastapi import HTTPException, status

def not_found(message: str = "Không tìm thấy dữ liệu") -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=message
    )

def bad_request(message: str = "Dữ liệu không hợp lệ") -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail=message
    )

def forbidden(message: str = "Bạn không có quyền thực hiện thao tác này") -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, 
        detail=message
    )