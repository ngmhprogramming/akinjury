from icrawler.builtin import GoogleImageCrawler

'''nosebleed_crawler = GoogleImageCrawler(storage={'root_dir': 'healine/nosebleed'})
nosebleed_crawler.crawl(keyword='nosebleed close-up', max_num=40, min_size=(200,200))
nosebleed_crawler.crawl(file_idx_offset=40, keyword='nosebleed', max_num=40, min_size=(200,200))
nosebleed_crawler.crawl(file_idx_offset=80, keyword='nose-bleed', max_num=10, min_size=(200,200))
nosebleed_crawler.crawl(file_idx_offset=90, keyword='nose bleed', max_num=10, min_size=(200,200))

contusion_crawler = GoogleImageCrawler(storage={'root_dir': 'healine/contusion'})
contusion_crawler.crawl(keyword='contusion', max_num=10, min_size=(200,200))
contusion_crawler.crawl(file_idx_offset=10, keyword='bruise', max_num=20, min_size=(200,200))
contusion_crawler.crawl(file_idx_offset=30, keyword='bruise close-up', max_num=20, min_size=(200,200))
contusion_crawler.crawl(file_idx_offset=50, keyword='arm bruise', max_num=10, min_size=(200,200))
contusion_crawler.crawl(file_idx_offset=60, keyword='arm contusion', max_num=10, min_size=(200,200))
contusion_crawler.crawl(file_idx_offset=70, keyword='knee bruise', max_num=10, min_size=(200,200))
contusion_crawler.crawl(file_idx_offset=80, keyword='leg contusion', max_num=10, min_size=(200,200))'''

burn_crawler = GoogleImageCrawler(storage={'root_dir': 'healine/firstdegburn'})
burn_crawler.crawl(keyword='first degree burn', max_num=50, min_size=(200,200))
burn_crawler.crawl(file_idx_offset=50, keyword='first degree burn', max_num=50, min_size=(200,200))

'''cut_crawler = GoogleImageCrawler(storage={'root_dir': 'healine/minorcut'})
cut_crawler.crawl(keyword='minor cut', max_num=100, min_size=(200,200))

snake_crawler = GoogleImageCrawler(storage={'root_dir': 'healine/snakebite'})
snake_crawler.crawl(keyword='snake bite', max_num=10, min_size=(200,200))
snake_crawler.crawl(file_idx_offset=10, keyword='snake bite wound', max_num=30, min_size=(200,200))'''
