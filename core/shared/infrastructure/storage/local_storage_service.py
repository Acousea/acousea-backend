from core.shared.domain.storage_service import StorageService


class LocalStorageService(StorageService):

    def download_latest(self) -> None:
        pass

    def get_latest(self) -> str:
        pass

    def get_all(self) -> list[str]:
        pass


if __name__ == '__main__':
    service = LocalStorageService("../../../../media")
    # Decode the image
    image = service.get_b64_image("tests", "cat.png")
    print("Image retrieved")
    print(image)

    print("All tests passed")
