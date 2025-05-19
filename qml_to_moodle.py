from logging import root
import xml.etree.ElementTree as ET
from xml.dom import minidom
import sys
from pathlib import Path
import os

def qml_to_moodle(qml_file, output_file):
    """Convert QML file to Moodle XML format"""
    try:
        # Parse QML file
        tree = ET.parse(qml_file)
        root = tree.getroot()

        # Create Moodle XML structure
        quiz = ET.Element('quiz')
        
        for qml_question in root.findall('QUESTION'):
            moodle_question = convert_question(qml_question)
            quiz.append(moodle_question)

        # Generate pretty XML
        xml_str = ET.tostring(quiz, encoding='utf-8')
        pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="  ")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(pretty_xml)
            
        print(f"Successfully converted to {output_file}")
        
    except Exception as e:
        print(f"Error during conversion: {str(e)}")

def convert_question(qml_question):
    """Convert individual QML question to Moodle XML format"""
    qtype = qml_question.find('ANSWER').get('QTYPE')
    
    if qtype == 'MC':
        return convert_multichoice(qml_question, single=True)
    elif qtype == 'MR':
        return convert_multichoice(qml_question, single=False)
    elif qtype == 'TF':
        return convert_truefalse(qml_question)
    elif qtype == 'OPEN':
        return convert_shortanswer(qml_question)
    elif qtype == 'NUM':
        return convert_numerical(qml_question)
    else:
        raise ValueError(f"Unsupported question type: {qtype}")

def convert_multichoice(qml_question, single):
    """Convert multiple choice question"""
    question = ET.Element('question', {'type': 'multichoice'})
    
    # Add name
    name = ET.SubElement(question, 'name')
    text = ET.SubElement(name, 'text')
    text.text = qml_question.get('DESCRIPTION')
    
    # Add question text
    questiontext = ET.SubElement(question, 'questiontext', {'format': 'html'})
    text = ET.SubElement(questiontext, 'text')
    content = qml_question.find('CONTENT')
    text.text = content.text if content.text else ''
    
    # Get correct answer ID
    correct_id = qml_question.find('OUTCOME').find('CONDITION').text.strip('"')
    
    # Add answers
    for choice in qml_question.find('ANSWER').findall('CHOICE'):
        answer = ET.SubElement(question, 'answer')
        fraction = '100' if choice.get('ID') == correct_id else '0'
        answer.set('fraction', fraction)
        
        text_elem = ET.SubElement(answer, 'text')
        text_elem.text = choice.find('CONTENT').text
        
        feedback = ET.SubElement(answer, 'feedback')
        feedback_text = ET.SubElement(feedback, 'text')
        feedback_text.text = 'Correct' if fraction == '100' else 'Incorrect'
    
    # Add settings
    ET.SubElement(question, 'shuffleanswers').text = '1'
    ET.SubElement(question, 'single').text = 'true' if single else 'false'
    ET.SubElement(question, 'answernumbering').text = 'abc'
    
    return question

# Additional conversion functions for other question types...
# (Similar structure for truefalse, shortanswer, numerical)

def convert_truefalse(qml_question):
    """Convert true/false question to Moodle XML format"""
    question = ET.Element('question', {'type': 'truefalse'})
    
    # Add name
    name = ET.SubElement(question, 'name')
    text = ET.SubElement(name, 'text')
    text.text = qml_question.get('DESCRIPTION')
    
    # Add question text
    questiontext = ET.SubElement(question, 'questiontext', {'format': 'html'})
    text = ET.SubElement(questiontext, 'text')
    content = qml_question.find('CONTENT')
    text.text = content.text if content.text else ''
    
    # Add general feedback
    generalfeedback = ET.SubElement(question, 'generalfeedback', {'format': 'html'})
    gf_text = ET.SubElement(generalfeedback, 'text')
    gf_text.text = ''
    
    # Get correct answer
    correct_answer = qml_question.find('OUTCOME').find('CONDITION').text.strip('"')
    
    # Add true answer
    true_answer = ET.SubElement(question, 'answer', {'fraction': '100' if correct_answer == 'true' else '0'})
    true_text = ET.SubElement(true_answer, 'text')
    true_text.text = 'true'
    true_feedback = ET.SubElement(true_answer, 'feedback')
    true_fb_text = ET.SubElement(true_feedback, 'text')
    true_fb_text.text = 'Vero' if correct_answer == 'true' else 'Falso'
    
    # Add false answer
    false_answer = ET.SubElement(question, 'answer', {'fraction': '100' if correct_answer == 'false' else '0'})
    false_text = ET.SubElement(false_answer, 'text')
    false_text.text = 'false'
    false_feedback = ET.SubElement(false_answer, 'feedback')
    false_fb_text = ET.SubElement(false_feedback, 'text')
    false_fb_text.text = 'Vero' if correct_answer == 'false' else 'Falso'
    
    return question
	
	
def convert_shortanswer(qml_question):
    """Convert short answer question to Moodle XML format"""
    question = ET.Element('question', {'type': 'shortanswer'})
    
    # Add name
    name = ET.SubElement(question, 'name')
    text = ET.SubElement(name, 'text')
    text.text = qml_question.get('DESCRIPTION')
    
    # Add question text
    questiontext = ET.SubElement(question, 'questiontext', {'format': 'html'})
    text = ET.SubElement(questiontext, 'text')
    content = qml_question.find('CONTENT')
    text.text = content.text if content.text else ''
    
    # Add general feedback
    generalfeedback = ET.SubElement(question, 'generalfeedback', {'format': 'html'})
    gf_text = ET.SubElement(generalfeedback, 'text')
    gf_text.text = ''
    
    # Get correct answer
    correct_answer = qml_question.find('OUTCOME').find('CONDITION').text.strip('"')
    
    # Add correct answer
    answer = ET.SubElement(question, 'answer', {'fraction': '100'})
    answer_text = ET.SubElement(answer, 'text')
    answer_text.text = correct_answer
    feedback = ET.SubElement(answer, 'feedback')
    fb_text = ET.SubElement(feedback, 'text')
    fb_text.text = 'Correct answer'
    
    # Add case sensitivity setting
    ET.SubElement(question, 'usecase').text = '0'  # Case insensitive
    
    return question
	
def convert_numerical(qml_question):
    """Convert numerical question to Moodle XML format"""
    question = ET.Element('question', {'type': 'numerical'})
    
    # Add name
    name = ET.SubElement(question, 'name')
    text = ET.SubElement(name, 'text')
    text.text = qml_question.get('DESCRIPTION')
    
    # Add question text
    questiontext = ET.SubElement(question, 'questiontext', {'format': 'html'})
    text = ET.SubElement(questiontext, 'text')
    content = qml_question.find('CONTENT')
    text.text = content.text if content.text else ''
    
    # Add general feedback
    generalfeedback = ET.SubElement(question, 'generalfeedback', {'format': 'html'})
    gf_text = ET.SubElement(generalfeedback, 'text')
    gf_text.text = ''
    
    # Get correct answer
    correct_answer = qml_question.find('OUTCOME').find('CONDITION').text.strip('"')
    
    # Add correct answer
    answer = ET.SubElement(question, 'answer', {'fraction': '100'})
    answer_text = ET.SubElement(answer, 'text')
    answer_text.text = correct_answer
    ET.SubElement(answer, 'tolerance').text = '0'  # No tolerance
    
    feedback = ET.SubElement(answer, 'feedback')
    fb_text = ET.SubElement(feedback, 'text')
    fb_text.text = 'Correct answer'
    
    # Add units (empty by default)
    units = ET.SubElement(question, 'units')
    ET.SubElement(units, 'unit')
    
    return question
	


if __name__ == '__main__':

    # Legge tutti i file QML nella cartella corrente
    # e li converte in file XML di Moodle
    for qml_file in Path('.').glob('*.qml'):
        # Salta se il file è già un file XML
        if qml_file.suffix == '.xml':
            continue
        # Salta se il file non è un file QML
        if qml_file.suffix != '.qml':
            continue

        # Converte il file QML in XML di Moodle
        # e lo salva con lo stesso nome ma con estensione .xml
        qml_to_moodle(qml_file, f"{qml_file}.xml")

    # Convert a specific QML file
    # qml_to_moodle('87097-01-caratteri_frequenze.qml', '87097-01-caratteri_frequenze.qml.xml')