from illust.domain.repository.illust_repository import IllustRepository


class ImageValidationService:
    def __init__(self, illust_repository: IllustRepository):
        self.illust_repository = illust_repository

    def is_image_belongs_to_book(self, title_image_name: str, book_id: int):
        illusts = self.illust_repository.find_all_by_book_id(book_id)
        return any(illust.image_url == title_image_name for illust in illusts)
