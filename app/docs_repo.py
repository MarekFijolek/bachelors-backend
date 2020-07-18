from git import Repo
import os

class DocsRepo:
    def __init__(self, docs_dir, docs_uri, force_clone=False):
        if os.path.exists(docs_dir):
            if not os.path.isdir(docs_dir):
                raise Exception("Given path to a file, not directory")
            if os.listdir(docs_dir):
                if os.path.isdir(os.path.join(docs_dir, ".git")):
                    if force_clone:
                        print(">> Repository exists, forcing clone")
                        self.clean_directory(docs_dir)
                        self.repo = Repo.clone_from(docs_uri, docs_dir)
                    else:
                        print(">> Repository exists, loading to the app")
                        self.repo = Repo(docs_dir)
                else:
                    print(">> Direcrtory is not empty, deleting its contents and cloning the documentation repo")
                    self.clean_directory(docs_dir)
                    self.repo = Repo.clone_from(docs_uri, docs_dir)
            else:
                print(">> Directory empty, cloning the documentation repo")
                self.repo = Repo.clone_from(docs_uri, docs_dir)
        else:
            print(">> Directory does not exists, creating and cloning the documentation repo")
            self.repo = Repo.clone_from(docs_uri, docs_dir)

        self.docs_dir = docs_dir
        self.docs_uri = docs_uri
        self.origin = self.repo.remotes.origin

    def clean_directory(self, dir):
        import shutil

        for filename in os.listdir(dir):
            file_path = os.path.join(dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                raise Exception("Failed to delete %s. Reason: %s:" % (file_path, e))

    def is_up_to_date(self):
        return self.origin.fetch()[0].flags == 4

    def update(self):
        self.origin.fetch()
        self.origin.pull()
    
    def get_version(self):
        all_tags_sorted = sorted(self.repo.tags, key=lambda t: t.commit.committed_datetime)
        return str(all_tags_sorted[-1])