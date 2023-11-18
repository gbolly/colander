import io
import os
import re
from math import ceil
from typing import Any

# import docx2txt
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from spacy import matcher as spacy_matcher, load
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

from src.constants import NAME_PATTERN, SKILLS, SECTIONS_IN_RESUME
from src.resume_parser.utils import parse_token

nlp = load("en_core_web_sm")
matcher = spacy_matcher.Matcher(nlp.vocab)


def extract_text_from_pdf(file):
    # https://www.blog.pythonlibrary.org/2018/05/03/exporting-data-from-pdfs-with-python/
    for page in PDFPage.get_pages(file.file, caching=True, check_extractable=True):
        resource_manager = PDFResourceManager()
        fake_file_handle = io.StringIO()
        converter = TextConverter(
            resource_manager, fake_file_handle, codec="utf-8", laparams=LAParams()
        )
        page_interpreter = PDFPageInterpreter(resource_manager, converter)
        page_interpreter.process_page(page)

        text = fake_file_handle.getvalue()
        yield text

        # close open handles
        converter.close()
        fake_file_handle.close()


# def extract_text_from_doc(doc_path):
#     '''
#     Helper function to extract plain text from .doc or .docx files

#     :param doc_path: path to .doc or .docx file to be extracted
#     :return: string of extracted text
#     '''
#     temp = docx2txt.process(doc_path)
#     text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
#     return ' '.join(text)


def extract_entity_sections(text):
    entities = {}
    key = False
    text_split = [i.strip() for i in text.split("\n")]
    for phrase in text_split:
        if len(phrase) == 1:
            p_key = phrase
        else:
            p_key = set(phrase.lower().split()) & set(SECTIONS_IN_RESUME)

        try:
            p_key = list(p_key)[0]
        except IndexError:
            pass

        if p_key in SECTIONS_IN_RESUME:
            entities[p_key] = []
            key = p_key
        elif key and phrase.strip():
            entities[key].append(phrase)

    return entities


def extract_name(nlp_text):
    patterns = [NAME_PATTERN]
    matcher.add("NAME", patterns)
    matches = matcher(nlp_text)

    for _, start, end in matches:
        span = nlp_text[start:end]
        return span.text


def extract_email(text):
    email = re.findall("([^@|\s]+@[^@]+\.[^@|\s]+)", text)
    if email:
        try:
            return email[0].split()[0].strip(";")
        except IndexError:
            return None


def extract_skills(nlp_text, noun_chunks):
    tokens = [token.text for token in nlp_text if not token.is_stop]
    # check for one-grams
    skillset = [token for token in tokens if token.lower() in SKILLS]
    skillset_bi_tri_gram = [
        parse_token(token.text)
        for token in noun_chunks
        if parse_token(token.text) in SKILLS
    ]
    skillset.extend(skillset_bi_tri_gram)
    skill_list = []
    for skill in set(skillset):
        if len(skill) == 3:
            skill_list.append(skill.upper())
        else:
            skill_list.append(skill.capitalize())
    return skill_list
    # return [skill.lower() for skill in set(skillset)]


def extract_experience(doc):
    experience_phrases = []
    for sentence in doc.sents:
        for token in sentence:
            if "experience" in token.text.lower():
                experience_phrases.append(sentence.text)
    return experience_phrases
    # wordnet_lemmatizer = WordNetLemmatizer()
    # stop_words = set(stopwords.words('english'))

    # # word tokenization
    # word_tokens = nltk.tokenize.word_tokenize(text)

    # # remove stop words and lemmatize
    # filtered_sentence = [w for w in word_tokens if not w in stop_words and wordnet_lemmatizer.lemmatize(w) not in stop_words]
    # tagged_sentence = nltk.tag.pos_tag(filtered_sentence)

    # # parse regex
    # cp = nltk.RegexpParser('P: {<NNP>+}')
    # cs = cp.parse(tagged_sentence)

    # test = []
    # for vp in list(cs.subtrees(filter=lambda x: x.label()=='P')):
    #     test.append(" ".join([i[0] for i in vp.leaves() if len(vp.leaves()) >= 2]))

    # # Search the word 'experience' in the chunk and then print out the text after it
    # x = [x[x.lower().index('experience') + 10:] for i, x in enumerate(test) if x and 'experience' in x.lower()]
    # return x


def jaccard_similarity(user_skill_set, job_skill_set):
    # Calculate Jaccard similarity between two sets of skills
    # to get the partial match score
    intersection = len(user_skill_set.intersection(job_skill_set))
    union = len(user_skill_set) + len(job_skill_set) - intersection
    similarity = intersection / union if union > 0 else 0.0

    return similarity


def skill_match_score(user_skills: list = [], job_skills: list = []) -> int:
    # score = jaccard_similarity(set(user_skills), set(job_skills))
    score = len(set(user_skills).intersection(job_skills))
    try:
        percentage_score = (score / len(job_skills)) * 100
    except:
        percentage_score = 1

    return ceil(percentage_score)


def resume_relevance_score(summary, jd):
    # Initialize the Tf-idf vectorizer
    vectorizer = TfidfVectorizer()
    corpus = " ".join(summary)
    # Fit and transform the corpus and job description
    tfidf_matrix = vectorizer.fit_transform([corpus, jd])
    # Calculate cosine similarity
    cosine_score = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]
    percentage_score = cosine_score * 100

    return ceil(percentage_score)


async def process_files(
    files: list, job_description: str, job_title: str
) -> dict[str, Any]:
    results = []

    for file in files:
        text = ""
        data = {}
        filename = file.filename
        extension = os.path.splitext(filename)[1]

        if extension == ".pdf":
            pages = extract_text_from_pdf(file)
            for page in pages:
                text += " " + page

        doc = nlp(text)
        data["names"] = extract_name(doc)
        data["email"] = extract_email(text)
        data["experience"] = extract_experience(doc)

        job_desc_doc = nlp(job_description)
        job_desc_skills = extract_skills(job_desc_doc, job_desc_doc.noun_chunks)
        skills = extract_skills(doc, doc.noun_chunks)
        skills_score = skill_match_score(skills, job_desc_skills)
        data["skills"] = skills
        data["skills_score"] = skills_score

        sections = extract_entity_sections(text)
        summary = sections.get("summary", "")
        relevance_score = resume_relevance_score(summary, job_title)
        data["resume_relevance_score"] = relevance_score
        data["summary"] = summary

        results.append(data)

    return results
