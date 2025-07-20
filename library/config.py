import json


class Config(dict):
    """支持嵌套字典自动保存的配置类"""

    def __init__(self, filepath='config.json', _internal_call=False):
        """
        初始化配置
        :param filepath: 配置文件路径，默认'config.json'
        :param _internal_call: 内部调用标识，避免递归加载
        """
        super().__init__()
        self.filepath = filepath

        # 只有最外层调用才加载文件
        if not _internal_call:
            self.load()

    def load(self):
        """从文件加载配置"""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.update(self._convert_dicts(data))
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def _convert_dicts(self, data):
        """递归将字典转换为Config实例"""
        if isinstance(data, dict):
            # 使用_internal_call=True避免递归加载文件
            new_dict = Config(self.filepath, _internal_call=True)
            for k, v in data.items():
                new_dict[k] = self._convert_dicts(v)
            return new_dict
        elif isinstance(data, list):
            return [self._convert_dicts(item) for item in data]
        else:
            return data

    def save(self):
        """保存配置到文件"""
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(dict(self), f, ensure_ascii=False, indent=4)

    def __setitem__(self, key, value):
        """设置值并自动保存"""
        super().__setitem__(key, self._convert_dicts(value))
        self.save()

    def __delitem__(self, key):
        """删除值并自动保存"""
        super().__delitem__(key)
        self.save()

    def clear(self):
        """清空配置并自动保存"""
        super().clear()
        self.save()

    def pop(self, key, *args):
        """弹出值并自动保存"""
        result = super().pop(key, *args)
        self.save()
        return result

    def popitem(self):
        """弹出项并自动保存"""
        result = super().popitem()
        self.save()
        return result

    def setdefault(self, key, default=None):
        """设置默认值并自动保存"""
        result = super().setdefault(key, default)
        self.save()
        return result

    def update(self, *args, **kwargs):
        """更新配置并自动保存"""
        super().update(*args, **kwargs)
        self.save()

    def __ior__(self, other):
        """支持|=运算符并自动保存"""
        result = super().__ior__(other)
        self.save()
        return result

    def __or__(self, other):
        """支持|运算符并自动保存"""
        result = super().__or__(other)
        if isinstance(result, Config):
            result.save()
        return result



def is_dict(s):
    try:
        result = json.loads(s)
        return isinstance(result, dict)
    except json.JSONDecodeError:
        return False

if __name__ == "__main__":
    config = Config("test_config.json")

    # 测试访问不存在的键
    print(config["nonexistent_key"])  # 返回空Config对象
    print(config.get("another_missing_key"))  # 返回None

    # 链式访问测试
    config["user"]["preferences"]["theme"] = "dark"
    print(config)