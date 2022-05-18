import json

class BookmarksDAO:

    def __init__(self, path):
        self.path = path

    def get_all_bookmarks(self):
        with open(self.path, 'r', encoding='utf-8') as bookmarks_file:
            bookmarks = json.load(bookmarks_file)
        return bookmarks

    def write_all_bookmarks(self, bookmarks):
        with open(self.path, 'w', encoding='utf-8') as bookmark_file:
            json.dump(bookmarks, bookmark_file, ensure_ascii=False, indent=4)

    def delete_bookmark_by_post_pk(self, post_pk):
        bookmarks = self.get_all_bookmarks()
        for idx, bookmark in enumerate(bookmarks):
            if bookmark.get('pk') == post_pk:
                del bookmarks[idx]
                break
        self.write_all_bookmarks(bookmarks)

    def check_bookmark_exists(self, bookmarks, new_bookmark):
        for bookmark in bookmarks:
            if bookmark.get('pk') == new_bookmark.get('pk'):
                return True  # Закладка существует
        return False

    def add_bookmark(self, new_bookmark):
        bookmarks = self.get_all_bookmarks()
        if not self.check_bookmark_exists(bookmarks, new_bookmark):
            bookmarks.append(new_bookmark)
            self.write_all_bookmarks(bookmarks)
            return new_bookmark
        return f'Закладка {new_bookmark} уже существует'



#bm_dao = BookmarksDAO('../../../data/bookmarks.json')
#bm = bm_dao.get_all_bookmarks()
##new_bm = {'pk':1, 'test':123}
#bm_dao.delete_bookmark_by_post_pk(1)
#print(bm_dao.add_bookmark({'pk':2, 'test':123}))
#print(bm_dao.check_bookmark_not_exist(bm, new_bm))

