import os

import weaviate


class WeaviateClient:
    def __init__(self, url: str, api_key: str):
        """
        初始化 Weaviate Client，指定 URL 和 API 密钥。

        :param url: Weaviate 的 URL
        :param api_key: API 密钥
        """
        self.client = weaviate.Client(
            url=url,
            auth_client_secret=weaviate.AuthApiKey(api_key=api_key)
        )

    def get_all_class_names(self) -> list:
        """
        获取 Weaviate 中所有的 class 名称。

        :return: 所有 class 名称的列表
        """
        try:
            schema = self.client.schema.get()
            class_names = [cls["class"] for cls in schema["classes"]]
            return class_names
        except Exception as e:
            raise Exception(f"Failed to fetch class names: {e}")

    def get_data_total_count(self, class_name: str) -> int:
        """
        获取特定类的数据总数。

        :param class_name: 类名
        :return: 数据总数
        """
        try:
            result = self.client.query.aggregate(class_name).with_meta_count().do()
            count = result['data']['Aggregate'][class_name][0]['meta']['count']
            return count
        except KeyError as e:
            raise Exception(f"Failed to fetch total count for class '{class_name}': {e}")

    def get_all_data(self, class_name: str) -> list:
        """
        获取全部数据（分页扫描）。

        :param class_name: 类名
        :return: 数据列表
        """
        all_data = []
        try:
            query = self.client.query.get(class_name, ["*"])
            result = query.with_limit(100).with_additional("id").do()

            while len(result['data']['Get'][class_name]) > 0:
                all_data.extend(result['data']['Get'][class_name])
                # 从最后一个 ID 继续扫描
                last_id = result['data']['Get'][class_name][-1]['_additional']['id']
                result = query.with_limit(100).with_where(
                    {
                        "operator": "GreaterThan",  # 从上次的最后一个位置继续查询
                        "path": ["id"],
                        "valueInt": int(last_id),
                    }
                ).do()

        except Exception as e:
            raise Exception(f"Failed to fetch all data for class '{class_name}': {e}")

        return all_data


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    url = os.getenv("WEAVIATE_ENDPOINT")
    key = os.getenv("WEAVIATE_API_KEY")
    print(url, key)
    c = WeaviateClient(url, key)
    print(c.get_all_class_names())
    print(c.get_all_data("Vector_index_4b8c8764_3493_49db_a12a_119ccc54cf71_Node"))