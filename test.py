import maltrieve
import requests


def test_basic_args():
    args = maltrieve.setup_args(['-l', 'maltrieve-test.log', '-p', '127.0.0.1:8080', '-d', '/opt/'])
    assert args.logfile == 'maltrieve-test.log'
    assert args.proxy == '127.0.0.1:8080'
    assert args.dumpdir == '/opt/'


def test_saving_args():
    args = maltrieve.setup_args(['-v', '-x', '-c', '-s'])
    assert args.viper
    assert args.vxcage
    assert args.cuckoo
    assert args.sort_mime


def test_parse_simple_list():
    source = requests.get('http://xwell.org/assets/maltrieve-test.txt').text
    assert maltrieve.process_simple_list(source) == \
        set(['http://example.org/mylist', 'http://example.com/yourlist'])


def test_parse_xml_list():
    source = requests.get('http://xwell.org/assets/maltrieve-test-list.xml').text
    assert maltrieve.process_xml_list_title(source) == \
        set(['http://example.org/mylist', 'http://example.com/yourlist'])


def test_parse_xml_desc():
    source = requests.get('http://xwell.org/assets/maltrieve-test-desc.xml').text
    assert maltrieve.process_xml_list_desc(source) == \
        set(['http://example.org/mylist', 'http://example.com/yourlist'])


def test_read_cfg():
    args = maltrieve.setup_args([])
    cfg = maltrieve.config(args, filename='maltrieve-test.cfg')
    assert cfg.logfile == 'maltrieve-test.log'
    assert cfg.dumpdir == '/tmp'
    assert cfg.black_list is None
    assert cfg.white_list is None
    assert cfg.useragent == "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 7.1; Trident/5.0)"


def test_override_cfg():
    args = maltrieve.setup_args(['-d', 'test-archive', '-l', 'another-test.log',
                                 '-p', '127.0.0.1:8080'])
    cfg = maltrieve.config(args, filename='maltrieve-test.cfg')
    assert cfg.proxy == {'http': '127.0.0.1:8080'}
    assert cfg.dumpdir == 'test-archive'
    assert cfg.logfile == 'another-test.log'


def test_load_hashes(hashfile='test-load-hashes.json'):
    assert maltrieve.load_hashes(hashfile) == \
        set(['d41d8cd98f00b204e9800998ecf8427e'])


def test_save_hashes():
    hashes = set(['d41d8cd98f00b204e9800998ecf8427e'])
    maltrieve.save_hashes(hashes, 'test-save-hashes.json')
    test_load_hashes('test-save-hashes.json')


def test_load_urls(urlfile='test-load-urls.json'):
    assert maltrieve.load_urls(urlfile) == \
        set(['http://example.com/badurl'])


def test_save_urls():
    urls = set(['http://example.com/badurl'])
    maltrieve.save_urls(urls, 'test-save-urls.json')
    test_load_urls('test-save-urls.json')


def test_get_sources():
    args = maltrieve.setup_args([])
    cfg = maltrieve.config(args, filename='maltrieve-test.cfg')
    source_lists = maltrieve.process_source_lists(cfg)
    assert len(source_lists) == len(cfg.source_urls)
