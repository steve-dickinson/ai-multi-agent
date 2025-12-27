import difflib
import re
from typing import List, Tuple

def generate_diff_html(text1: str, text2: str) -> str:
    """
    Generates a simple HTML diff of two texts.
    """
    d = difflib.HtmlDiff()
    # We use a very basic table style
    return d.make_file(text1.splitlines(), text2.splitlines(), context=True, numlines=2)

def analyze_tone(text: str) -> str:
    """
    Returns HTML string with tone issues highlighted.
    - Red: Passive Voice
    - Yellow: Complex Sentences (> 25 words)
    - Blue: Complex Words
    """
    
    # Simple heuristics
    passive_voice_patterns = [
        r"\b(am|is|are|was|were|be|been|being)\s+\w+(ed|en)\b"
    ]
    
    complex_words = [
        "accordingly", "consequently", "furthermore", "however", "moreover", "nevertheless", "nonetheless", "therefore", "thus",
        "utilize", "facilitate", "implement", "leverage", "optimize", "streamline"
    ]
    
    # Split into sentences for length check
    sentences = re.split(r'(?<=[.!?])\s+', text)
    processed_sentences = []
    
    for sentence in sentences:
        words = sentence.split()
        highlighted_sentence = sentence
        
        # 1. Check Length
        if len(words) > 25:
            highlighted_sentence = f"<span style='background-color: #fff3cd; padding: 2px; border-radius: 3px;' title='Long Sentence ({len(words)} words)'>{highlighted_sentence}</span>"
            
        # 2. Check Passive Voice (Regex)
        for pattern in passive_voice_patterns:
            matches = list(re.finditer(pattern, highlighted_sentence, re.IGNORECASE))
            # Go backwards to check indices don't shift? Or just replace string?
            # String replace is risky if words appear twice. 
            # Let's simple string replace for demo purposes, fully robust is hard without NLP lib like Spacy.
            # We will use regex sub with a callback to wrap matches.
            pass
            
        highlighted_sentence = re.sub(
            r"\b(am|is|are|was|were|be|been|being)\s+(\w+(?:ed|en))\b", 
            r"<span style='background-color: #f8d7da; color: #721c24; padding: 2px;' title='Passive Voice'>\g<0></span>", 
            highlighted_sentence, 
            flags=re.IGNORECASE
        )
            
        # 3. Check Complex Words
        for word in complex_words:
             # Basic case insensitive replace
             highlighted_sentence = re.sub(
                 rf"\b{word}\b",
                 f"<span style='background-color: #d1ecf1; color: #0c5460; padding: 2px;' title='Complex Word'>{word}</span>",
                 highlighted_sentence,
                 flags=re.IGNORECASE
             )
             
        processed_sentences.append(highlighted_sentence)
        
    return " ".join(processed_sentences)
