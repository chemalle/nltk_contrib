
# Natural Language Toolkit: Gale-Church Aligner Utilities
#
# Copyright (C) 2001-2010 NLTK Project
# Author: Chris Crowner <ccrowner@gmail.com>
# URL: <http://nltk.org/>
# For license information, see LICENSE.TXT

# Utility Functions

def readlines(filename):  
    lines = []
    
    input_file = file(filename, "r")
    substrings = []
    file_text = input_file.read()
    
    raw_lines = file_text.split('\n')
    lines = [line for line in raw_lines if not(line.strip() == '')]
                        
    return lines
    
def get_regions(lines, hard_delimiter, soft_delimiter):
    hard_regions = []          
    soft_regions = []
    soft_region = []        
    
    for line in lines:          
      if not(line.find(hard_delimiter) == -1) and (soft_regions):          
          hard_regions.append(soft_regions)           
          soft_regions = [] 
      elif not(line.find(soft_delimiter) == -1) and (soft_region):          
          soft_regions.append(soft_region)
          soft_region = []
      else:
          soft_region.append(line)
    
    if (soft_regions):
        hard_regions.append(soft_regions) 
    
    return hard_regions 
    
def get_paragraphs_sentences(lines, para_delimiter, sent_delimiter):
    paragraphs = []          
    sentences = []
    sentence = ''        
    
    for line in lines:          
      if not(line.find(para_delimiter) == -1) and (sentences):          
          paragraphs.append(sentences)           
          sentences = [] 
      elif not(line.find(sent_delimiter) == -1) and (sentence):          
          sentences.append(sentence)
          sentence = ''
      else:
          if sentence:
              sentence = sentence + ' ' + line
          else:
              sentence = line
    
    if (sentences):
        paragraphs.append(sentences) 
    
    return paragraphs      

def get_character_lengths(region):
    character_lengths = []    
    
    for soft_reg in region:
        len_lines = 0
        for line in soft_reg:
            len_lines = len_lines + len(line)
            
        character_lengths.append(len_lines)
        
    return character_lengths
    
def convert_bead_to_tuples(alignments, hard_region1, hard_region2):
    alignment_mapping = []
    for soft_key in alignments.keys():        
        alignment = alignments[soft_key]        
        if (alignment.category == '1 - 1'):
            align_tuple = (list_to_str(hard_region1[soft_key]), list_to_str(hard_region2[soft_key]))
            alignment_mapping.append(align_tuple)                    
        elif (alignment.category == '1 - 0'):
            align_tuple = (list_to_str(hard_region1[soft_key]), '')
            alignment_mapping.append(align_tuple)
        elif (alignment.category == '0 - 1'):
            align_tuple = ('', list_to_str(hard_region2[soft_key]))
            alignment_mapping.append(align_tuple)
        elif (alignment.category == '2 - 1'):
            align_tuple = (list_to_str(hard_region1[soft_key]), list_to_str(hard_region2[soft_key]))
            alignment_mapping.append(align_tuple)
            align_tuple = (list_to_str(hard_region1[soft_key + 1]), list_to_str(hard_region2[soft_key]))
            alignment_mapping.append(align_tuple)
        elif (alignment.category == '1 - 2'):
            align_tuple = (list_to_str(hard_region1[soft_key]), list_to_str(hard_region2[soft_key]))
            alignment_mapping.append(align_tuple)
            align_tuple = (list_to_str(hard_region1[soft_key]), list_to_str(hard_region2[soft_key + 1]))
            alignment_mapping.append(align_tuple)
        elif (alignment.category == '2 - 2'):
            align_tuple = (list_to_str(hard_region1[soft_key]), list_to_str(hard_region2[soft_key]))
            alignment_mapping.append(align_tuple)
            align_tuple = (list_to_str(hard_region1[soft_key + 1]), list_to_str(hard_region2[soft_key + 1]))
            alignment_mapping.append(align_tuple)
        else:
            print "not supported alignment type"
    
    return alignment_mapping
    
def list_to_str(input_list):
    return input_list
    #return ' '.join([item for item in input_list])

def get_alignment_links(alignments):
    alignment_mappings = []
    hard_key = 0
    for hard_list in alignments:        
        for alignment_dict in hard_list:            
            for align_key in alignment_dict.keys():
                alignment = alignment_dict[align_key]
    
                if (alignment.category == '1 - 1'):
                    align_triple = (hard_key,
                                    align_key,
                                    align_key)
                    alignment_mappings.append(align_triple)
                elif (alignment.category == '1 - 0'):
                    align_triple = (hard_key,
                                    align_key,
                                    -1)
                    alignment_mappings.append(align_triple)
                elif (alignment.category == '0 - 1'):
                    align_triple = (hard_key,
                                    -1,
                                    align_key)
                    alignment_mappings.append(align_triple)
                elif (alignment.category == '2 - 1'):
                    align_triple = (hard_key,
                                    align_key + 1,
                                    align_key)        
                    alignment_mappings.append(align_triple)
                    align_triple = (hard_key,
                                    align_key,
                                    align_key)
                    alignment_mappings.append(align_triple)
                elif (alignment.category == '1 - 2'):
                    align_triple = (hard_key,
                                    align_key,
                                    align_key + 1)            
                    alignment_mappings.append(align_triple)
                    align_triple = (hard_key,
                                    align_key,
                                    align_key)
                    alignment_mappings.append(align_triple)
                elif (alignment.category == '2 - 2'):
                    align_triple = (hard_key,
                                    align_key + 1,
                                    align_key + 1)            
                    alignment_mappings.append(align_triple)
                    align_triple = (hard_key,
                                    align_key,
                                    align_key)
                    alignment_mappings.append(align_triple)
                else:
                    print "not supported alignment type"
                
    return alignment_mappings
    
def get_test_values(alignments):
    test_values = []
    for hard_regions_index in alignments.keys():
        soft_regions_list = []
        for soft_regions_index in alignments[hard_regions_index].keys():
            soft_regions_list.extend(alignments[hard_regions_index][soft_regions_index].alignment_mappings) 
        soft_regions_list.reverse()
        test_values.extend(soft_regions_list)
        
    return test_values
    
def get_reference_values(filename):
    input_file = file(filename, "r")
    reference_values = []
    
    raw_lines = input_file.read().split('\n')
    lines = [line for line in raw_lines if not(line.strip() == '')]
    
    for line in lines:                
        line_parts = line.split(',')        
        reference_values.append((int(line_parts[0]),int(line_parts[1]),int(line_parts[2])))
    
    return reference_values
    
    
