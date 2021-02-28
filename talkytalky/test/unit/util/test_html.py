from talkytalky.util.html import assign_sentence_ids, extract_paragraphs
from talkytalky.util.util import make_dir, get_project_root


def test_assign_ids_call_wild_ch_1():
    project_root = get_project_root()
    print(project_root)
    in_file = project_root + "/test/exploded_epubs/call_of_the_wild/OEBPS/@public@vhost@g@gutenberg@html@files@215@215-h@215-h-1.htm.html"
    out_dir =  project_root + "/test/temp/util/html/"
    make_dir(out_dir)
    out_file = out_dir + '/' + "call_of_the_wild_ch_1_with_sentence_ids.html"
    assign_sentence_ids(in_file, out_file)


def test_assign_sentence_ids_peter_rabbit():
    project_root = get_project_root()
    print(project_root)
    in_file = project_root + "/test/exploded_epubs/peter_rabbit/OEBPS/@public@vhost@g@gutenberg@html@files@14838@14838-h@14838-h-0.htm.html"
    out_dir =  project_root + "/test/temp/util/html/"
    make_dir(out_dir)
    out_file = out_dir + '/' + "peter_rabbit_with_sentence_ids.html"
    assign_sentence_ids(in_file, out_file)


def test_assign_sentence_ids_house_that_jack_built():
    project_root = get_project_root()
    print(project_root)
    in_file = project_root + "/test/exploded_epubs/the_house_that_jack_built_no_images/OEBPS/@public@vhost@g@gutenberg@html@files@12109@12109-h@12109-h-0.htm.html"
    out_dir =  project_root + "/test/temp/util/html/"
    make_dir(out_dir)
    out_file = out_dir + '/' + "house_that_jack_built_with_sentence_ids.html"
    assign_sentence_ids(in_file, out_file)


def test_assign_sentence_ids_call_of_the_wild_excerpt():
    project_root = get_project_root()
    print(project_root)
    in_file = project_root + "/test/exploded_epubs/call_of_the_wild_excerpt/EPUB/The_Call_of_the_Wild-2.xhtml"
    out_dir =  project_root + "/test/temp/util/html/"
    make_dir(out_dir)
    out_file = out_dir + '/' + "call_of_the_wild_excerpt_with_sentence_ids.html"
    assign_sentence_ids(in_file, out_file)


def test_extract_paragraphs():
    project_root = get_project_root()
    print(project_root)
    in_file = project_root + "/test/exploded_epubs/peter_rabbit/OEBPS/@public@vhost@g@gutenberg@html@files@14838@14838-h@14838-h-0.htm.html"
    paragraphs = extract_paragraphs(in_file)
    assert paragraphs is not None
    assert len(paragraphs)
    print(paragraphs)

