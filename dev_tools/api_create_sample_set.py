from api_dev_tools import PodcastIndexConfig, PodcastIndexAPI, ValidQueriesExtractor, BatchAPICaller, OutputHandler


def create_sample_JSONs():
    config_instance = PodcastIndexConfig()
    api_instance = PodcastIndexAPI(config_instance.config)

    valid_query_extractor = ValidQueriesExtractor(api_instance) 
    valid_query_extractor.get_all_valid_fields()

    output_handler = OutputHandler()
    
    batch_api_caller = BatchAPICaller(api_instance, valid_query_extractor.valid_queries)
    batch_api_caller.download_sample_set()


if __name__ == "__main__":
    create_sample_JSONs()
    

