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
                size = float(prev) + float(pres)
                hash_map.put(file.repo_name, cnt[0] + 1, round(size, 3), file)
        return hash_map
