import xml.etree.ElementTree as ET
from xml.dom import minidom

NS_SMIL = 'http://www.w3.org/ns/SMIL'
NS_EPUB = 'http://www.idpf.org/2007/ops'


def generate_smil(sentence_pairs, text_source, audio_source, outfile):

    ET.register_namespace('', NS_SMIL)
    ET.register_namespace('epub', NS_EPUB)

    # Generate XML header
    smil = ET.Element('{%s}smil' % NS_SMIL, {'version': '3.0'})
    body = ET.SubElement(smil, '{%s}body' % NS_SMIL)

    # TODO: textref is supposed to reflect the section that encloses all the text in the sequence
    seq = ET.SubElement(body, '{%s}seq' % NS_SMIL, {'{%s}textref' % NS_EPUB: text_source})

    par_index = 1

    for pair in sentence_pairs:
        par = ET.SubElement(seq, '{%s}par' % NS_SMIL, {'id': 'par_%d' % par_index})

        # Going on the assumption that the pair order is (text, audio)
        ET.SubElement(par, '{%s}text' % NS_SMIL, {'src': '%s#%s' % (text_source, pair[0].element_id)})
        ET.SubElement(par, '{%s}audio' % NS_SMIL,
                      {'src': '%s' % audio_source,
                       'clipBegin': '%.2f' % pair[1].start_time,
                       'clipEnd': '%.2f' % pair[1].end_time,
                       })
        par_index += 1

    document = ET.ElementTree(smil)
    document.write(outfile, xml_declaration=True, encoding='UTF-8')


def generate_lcs_based_smil(html_document, text_source, audio_source, outfile):

    ET.register_namespace('', NS_SMIL)
    ET.register_namespace('epub', NS_EPUB)

    # Generate XML header
    smil = ET.Element('{%s}smil' % NS_SMIL, {'version': '3.0'})
    body = ET.SubElement(smil, '{%s}body' % NS_SMIL)

    # TODO: textref is supposed to reflect the section that encloses all the text in the sequence
    seq = ET.SubElement(body, '{%s}seq' % NS_SMIL, {'{%s}textref' % NS_EPUB: text_source})

    par_index = 1

    for sentence in html_document.sentences:
        if sentence.audio_end() > 0.0 and sentence.audio_start() > 0.0:
            par = ET.SubElement(seq, '{%s}par' % NS_SMIL, {'id': 'par_%d' % par_index})

            # Going on the assumption that the pair order is (text, audio)
            ET.SubElement(par, '{%s}text' % NS_SMIL, {'src': '%s#%s' % (text_source, sentence.element_id)})
            ET.SubElement(par, '{%s}audio' % NS_SMIL,
                          {'src': '%s' % audio_source,
                           'clipBegin': '%.2f' % sentence.audio_start(),
                           'clipEnd': '%.2f' % sentence.audio_end(),
                           })
            par_index += 1

    document = ET.ElementTree(smil)
    document.write(outfile, xml_declaration=True, encoding='UTF-8')