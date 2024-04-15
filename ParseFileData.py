from HashMap import HashMap


class ParseFileData:

    def remake(self, files_array):
        hash_map = HashMap()
        for file in files_array:
            if not hash_map.contains_key(file.repo_name):
                hash_map.put(file.repo_name, 1, file.size, file)
            else:
                cnt = hash_map.get(file.repo_name)
                prev = cnt[1]
                pres = file.size
                if isinstance(cnt[1], str):
                    prev = ''.join(filter(str.isdigit, cnt[1]))
                if isinstance(file.size, str):
                    pres = ''.join(filter(str.isdigit, file.size))
                size = (float(prev)) + (float(pres))
                size = round(size, 3)
                hash_map.put(file.repo_name, cnt[0] + 1, size, file)
        return hash_map

    def remakeRepo(self, files_array, pos):
        hash_map = HashMap()
        for file in files_array:
            file_path = file.path.split('/')
            if len(file_path) >= pos:
                if not hash_map.contains_key(file_path[pos - 1]):
                    hash_map.put(file_path[pos - 1], 1, file.size, file)
                    print(file_path[pos - 1])
        return hash_map

    def remakeRepoByName(self, files_array, file_name, pos):
        hash_map = HashMap()
        for file in files_array:
            file_path = file.path.split('/')
            if len(file_path) >= pos:
                if file_path[pos - 2] == file_name and not hash_map.contains_key(file_path[pos - 2]):
                    hash_map.put(file_path[pos - 1], 1, file.size, file)
                    print(file_path[pos - 1])
        return hash_map
