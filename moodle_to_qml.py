import xml.etree.ElementTree as ET
from xml.dom import minidom

def moodle_to_qml(moodle_file, output_file):
    """Convert Moodle XML file to QML format"""
    try:
        # Parse Moodle XML
        tree = ET.parse(moodle_file)
        root = tree.getroot()

        # Create QML structure
        qml = ET.Element('QML')
        
        for moodle_question in root.findall('question'):
            qml_question = convert_to_qml_question(moodle_question)
            qml.append(qml_question)

        # Generate XML with doctype
        xml_str = ET.tostring(qml, encoding='utf-8')
        pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="  ")
        pretty_xml = pretty_xml.replace(
            '<?xml version="1.0" ?>',
            '<?xml version="1.0" standalone="no"?>\n<!DOCTYPE QML SYSTEM "QML_V3.dtd">'
        )
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(pretty_xml)
            
        print(f"Successfully converted to {output_file}")
        
    except Exception as e:
        print(f"Error during conversion: {str(e)}")

def convert_to_qml_question(moodle_question):
    """Convert Moodle question to QML format"""
    qtype = moodle_question.get('type')
    
    if qtype == 'multichoice':
        single = moodle_question.find('single').text == 'true'
        return convert_mc_to_qml(moodle_question, 'MC' if single else 'MR')
    elif qtype == 'truefalse':
        return convert_tf_to_qml(moodle_question)
    elif qtype == 'shortanswer':
        return convert_open_to_qml(moodle_question)
    elif qtype == 'numerical':
        return convert_num_to_qml(moodle_question)
    else:
        raise ValueError(f"Unsupported question type: {qtype}")

def convert_mc_to_qml(moodle_question, qml_type):
    """Convert multiple choice question to QML"""
    qml_question = ET.Element('QUESTION', {
        'ID': f"Q{hash(moodle_question.find('name').text)}",
        'DESCRIPTION': moodle_question.find('name').text,
        'TOPIC': 'converted',
        'STATUS': 'Normal'
    })
    
    # Add content
    content = ET.SubElement(qml_question, 'CONTENT', {'TYPE': 'text/html'})
    content.text = moodle_question.find('questiontext/text').text
    
    # Add answer choices
    answer = ET.SubElement(qml_question, 'ANSWER', {'QTYPE': qml_type})
    
    correct_answer = None
    for moodle_answer in moodle_question.findall('answer'):
        choice_id = f"C{hash(moodle_answer.find('text').text)}"
        choice = ET.SubElement(answer, 'CHOICE', {'ID': choice_id})
        choice_content = ET.SubElement(choice, 'CONTENT', {'TYPE': 'text/html'})
        choice_content.text = moodle_answer.find('text').text
        
        if moodle_answer.get('fraction') == '100':
            correct_answer = choice_id
    
    # Add outcome
    outcome = ET.SubElement(qml_question, 'OUTCOME', {
        'ID': f"O{hash(moodle_question.find('name').text)}",
        'SCORE': '1'
    })
    condition = ET.SubElement(outcome, 'CONDITION')
    condition.text = f'"{correct_answer}"'
    
    return qml_question

# Additional conversion functions for other question types...

if __name__ == '__main__':
    moodle_to_qml('moodle_questions.xml', 'converted_qml.xml')