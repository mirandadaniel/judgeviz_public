import pytest  
import app   
import unittest 
from unittest import mock
import pandas as pd
from sqlalchemy import create_engine

class TestHighlightRoles(unittest.TestCase):
    def setUp(self):
        app.selected_roles_list = ['framing', 'fact']
 
    def test_highlight_roles(row):
        app.hr.selected_roles_list = 'fact'
        data = {'role': ['FRAMING'], 'case_text': ['blah blah']}
        df = pd.DataFrame(data)
        row = df.iloc[0]
        colour = app.hr.highlight_roles(row)
        colour_test = ['background-color: ' for r in row]
        assert colour == colour_test
    
    def test_highlight_roles2(row):
        app.hr.selected_roles_list = 'fact'
        data = {'role': ['FACT'], 'case_text': ['blah blah']}
        df = pd.DataFrame(data)
        row = df.iloc[0]
        colour = app.hr.highlight_roles(row)
        colour_test = ['background-color: #deb6f0' for r in row]
        assert colour == colour_test
    
    def test_highlight_roles3(row):
        app.hr.selected_roles_list = 'disposal'
        data = {'role': ['DISPOSAL'], 'case_text': ['blah blah']}
        df = pd.DataFrame(data)
        row = df.iloc[0]
        colour = app.hr.highlight_roles(row)
        colour_test = ['background-color: #b9fabb' for r in row]
        assert colour == colour_test
    
    def test_highlight_roles4(row):
        app.hr.selected_roles_list = ' '
        data = {'role': ['FACT'], 'case_text': ['blah blah']}
        df = pd.DataFrame(data)
        row = df.iloc[0]
        colour = app.hr.highlight_roles(row)
        colour_test = ['background-color: ' for r in row]
        assert colour == colour_test

    def test_remove_irrelevant_sentences(self):
        data = {'role': ['NAN', 'FRAMING', 'FACT', 'BACKGROUND'],
        'case_text': ['LADY HALE', 'test2', 'test3', 'test4']}
        df = pd.DataFrame(data)
        comp_data = {'role': ['NAN', 'FRAMING', 'FACT'],
        'case_text': ['LADY HALE', 'test2', 'test3']}
        comp_df = pd.DataFrame(comp_data)
        comp_len = len(comp_df)
        selected_roles_list = ['framing', 'fact']
        df = app.hr.remove_irrelevant_sentences(df, selected_roles_list)
        df_len = len(df)
        assert df_len == comp_len

    def test_remove_irrelevant_sentences2(self):
        data = {'role': ['NAN', 'DISPOSAL', 'FACT', 'BACKGROUND'],
        'case_text': ['LADY HALE', 'test2', 'test3', 'test4']}
        df = pd.DataFrame(data)
        comp_data = {'role': ['NAN', 'DISPOSAL', 'FACT'],
        'case_text': ['LADY HALE', 'test2', 'test3']}
        comp_df = pd.DataFrame(comp_data)
        comp_len = len(comp_df)
        selected_roles_list = ['disposal', 'fact']
        df = app.hr.remove_irrelevant_sentences(df, selected_roles_list)
        df_len = len(df)
        assert df_len == comp_len

class TestMakeGraph(unittest.TestCase):  
    def testGetJudgeNames(self): 
        data = ['lady hale', 'lord steyn', 'lord hoffmann']
        df = pd.DataFrame(data, columns=['from_col'])
        all_judges_temp = app.mg.get_judge_names(df)
        all_judges_test = ['hale', 'steyn', 'hoffmann']
        assert all_judges_temp == all_judges_test
    
    def testTrimJudge(self):
        full_name = 'lady hale'
        test_name = 'hale'
        check_name = app.mg.trim_judge(full_name)
        assert check_name == test_name
    
    def testTrimJudge2(self):
        full_name = 'all'
        test_name = 'all'
        check_name = app.mg.trim_judge(full_name)
        assert check_name == test_name
    
    def testTrimJudge3(self):
        full_name = 'self'
        test_name = None
        check_name = app.mg.trim_judge(full_name)
        assert check_name == test_name

    def testCheckMo(self):
        data = {'mj_col': ['lady hale']}
        df = pd.DataFrame(data)
        row = df.iloc[0]
        check_mo = ['lady hale']
        test_mo = app.mg.check_mo(row)
        assert test_mo == check_mo
    
    def testCheckMo2(self):
        data = {'mj_col': ['lady hale, lord steyn, lord hoffmann']}
        df = pd.DataFrame(data)
        row = df.iloc[0]
        check_mo = ['lady hale', ' lord steyn', ' lord hoffmann']
        test_mo = app.mg.check_mo(row)
        assert test_mo == check_mo
    
    def test_check_mo3(self):
        app.c.mo_judges = []
        data = {'mj_col': ['lady hale']}
        df = pd.DataFrame(data)
        row = df.iloc[0]
        app.mg.check_mo(row)
        check_c_mo = ['Lady Hale']
        assert app.c.mo_judges == check_c_mo
    
    def test_check_mo4(self):
        app.c.mo_judges = []
        data = {'mj_col': ['lady hale, lord steyn, lord hoffmann']}
        df = pd.DataFrame(data)
        row = df.iloc[0]
        app.mg.check_mo(row)
        check_c_mo = ['Lady Hale', ' Lord Steyn', ' Lord Hoffmann']
        assert app.c.mo_judges == check_c_mo
    
    def test_line_check(self):
        data = {'relation_col': ['fullagr']}
        df = pd.DataFrame(data)
        row = df.iloc[0]
        assert app.mg.line_check(row) == True
    

    def test_line_check2(self):
        data = {'relation_col': ['NAN']}
        df = pd.DataFrame(data)
        row = df.iloc[0]
        assert app.mg.line_check(row) == False
    
    def test_populate_dict(self):
        app.c.judge_dict = []
        data = [['lady hale', 'lord steyn', 'fullagr', '2']]
        df = pd.DataFrame(data, columns=['from_col', 'to_col', 'relation_col', 'line_col'])
        row = df.iloc[0]
        test_dict = [{ 'from': 'lady hale', 
            'to': 'lord steyn',
            'relation': 'fullagr',
            'line_number': '2'}]
        app.mg.populate_dict(row)
        assert app.c.judge_dict == test_dict
    
    def test_populate_dict2(self):
        app.c.judge_dict = []
        data = [['lord browne-wilkinson', 'self', 'outcome', '7']]
        df = pd.DataFrame(data, columns=['from_col', 'to_col', 'relation_col', 'line_col'])
        row = df.iloc[0]
        test_dict = [{ 'from': 'lord browne-wilkinson', 
            'to': 'self',
            'relation': 'outcome',
            'line_number': '7'}]
        app.mg.populate_dict(row)
        assert app.c.judge_dict == test_dict

    def test_make_line_no_mo(self):
        line_check = ' \"hale\" [shape="circle", fixedsize="true", height=1, width=1, style="filled", fillcolor="white", href="#hale"]; \n' 
        judge = '\"lady hale\"'
        line = app.mg.make_line_no_mo(judge)
        assert line == line_check

class TestFormatDataframe(unittest.TestCase):
    def test_agr(self):
        test_sentence = "Full agreement from Lady Hale to Lord Hoffmann"
        from_col = 'lady hale'
        to = 'lord hoffmann'
        rel = 'fullagr'
        body = 'I fully agree with Lord Hoffmann'
        prev_label = 'NAN'
        prev_judge_from = 'lord steyn'
        assert app.fd.format_fullagr(from_col, to, rel, body, prev_label, prev_judge_from) == test_sentence

    def test_agr2(self):
        test_sentence = "Full agreement from Lady Hale to Lord Steyn, full agreement from Lady Hale to Lord Hoffmann"
        from_col = 'Lady Hale'
        to = 'Lord Hoffmann'
        rel = 'fullagr'
        body = 'I fully agree with Lord Hoffmann'
        prev_label = 'Full agreement from Lady Hale to Lord Steyn'
        prev_judge_from = 'Lady Hale'
        assert app.fd.format_fullagr(from_col, to, rel, body, prev_label, prev_judge_from) == test_sentence

    def test_partagr(self):
        test_sentence = "Partial agreement from lady hale to lord hoffmann"
        from_col = 'lady hale'
        to = 'lord hoffmann'
        rel = 'partagr'
        body = 'I partially agree with Lord Hoffmann'
        prev_label = 'NAN'
        prev_judge_from = 'Lord Steyn'
        assert app.fd.format_partagr(from_col, to, rel, body, prev_label, prev_judge_from) == test_sentence

    def test_dis(self):
        test_sentence = "Full disagreement from lady hale to lord hoffmann"
        from_col = 'lady hale'
        to = 'lord hoffmann'
        rel = 'fulldis'
        body = 'I fully disagree with Lord Hoffmann'
        prev_label = 'NAN'
        prev_judge_from = 'Lord Hoffmann'
        assert app.fd.format_fulldis(from_col, to, rel, body, prev_label, prev_judge_from) == test_sentence

    def test_part_dis(self):
        test_sentence = "Partial disagreement from lady hale to lord hoffmann"
        from_col = 'lady hale'
        to = 'lord hoffmann'
        rel = 'partdis'
        body = 'I partially disagree with Lord Hoffmann'
        prev_label = 'NAN'
        prev_judge_from = 'Lord Hope'
        assert app.fd.format_partdis(from_col, to, rel, body, prev_label, prev_judge_from) == test_sentence
    
    def test_outcome(self):
        test_sentence = "Agreement on outcome from lady hale to self"
        from_col = 'lady hale'
        to = 'self'
        rel = 'outcome'
        body = 'I agree on the outcome with myself'
        prev_label = 'NAN'
        prev_judge_from = 'Lord Mance'
        assert app.fd.format_outcome(from_col, to, rel, body, prev_label, prev_judge_from) == test_sentence

    def test_outcome_w_prev_label(self):
        test_sentence = "Full agreement from Lady Hale to Lord Hoffmann, agreement on outcome from Lady Hale to self"
        from_col = 'Lady Hale'
        to = 'self'
        rel = 'outcome'
        body = 'I agree on the outcome with myself'
        prev_label = 'Full agreement from Lady Hale to Lord Hoffmann'
        prev_judge_from = 'Lady Hale'
        assert app.fd.format_outcome(from_col, to, rel, body, prev_label, prev_judge_from) == test_sentence

    def test_get_case_names(self):
        case_titles = app.get_case_names()
        assert case_titles[0] == 'Case 22 : Eastbourne Town Radio Cars Association v Commissioners of Customs & Excise (UKHL) 2001' 
        assert case_titles[20] == 'Case 26 : J A Pye (Oxford) Ltd and others v Graham and another (UKHL) 2002' 

    def test_capitalize_judge(self):
        judge_name = 'lord hoffmann'
        assert app.fd.capitalize_judge(judge_name) == 'Lord Hoffmann'
    
    def test_capitalize_judge2(self):
        judge_name = 'self'
        assert app.fd.capitalize_judge(judge_name) == 'self'
    
    def test_format_sentence(self):
        test_sentence = "Full agreement from Lady Hale to Lord Hoffmann, agreement on outcome from Lady Hale to self"
        from_col = 'lady hale'
        to = 'self'
        rel = 'outcome'
        body = 'I agree on the outcome with myself'
        prev_label = 'Full agreement from Lady Hale to Lord Hoffmann'
        prev_judge_from = 'Lady Hale'
        assert app.fd.format_sentence(from_col, to, rel, body, prev_label, prev_judge_from) == test_sentence

    def test_remove_htm(self):
        data = [['www.google.htm'], ['My lords, ']]
        df = pd.DataFrame(data, columns=['body'])
        check_length = 1
        df = app.fd.remove_htm(df)
        assert check_length == len(df)
    
    def test_add_heading_tags(self):
        app.c.all_judges = ['lady hale', 'lord browne-wilkinson']
        data = [['LORD BROWNE-WILKINSON'], ['My lords, I am here today to say...']]
        df = pd.DataFrame(data, columns=['body'])
        df = app.fd.add_heading_tags(df)
        cell = df.iloc[0]['body']
        check_data = [['<p id="lord browne-wilkinson";><b>LORD BROWNE-WILKINSON</b> </p>'], ['My lords, I am here today to say...']]
        check_df = pd.DataFrame(check_data, columns=['body'])
        check_cell = check_df.iloc[0]['body']
        assert check_cell == cell
    
    def test_add_html_tags(self):
        data = [['I agree fully with Lady Hale.', 'fullagr', '100']]
        df = pd.DataFrame(data, columns=['body', 'relation_col', 'line_col'])
        df = app.fd.add_html_tags(df)
        cell = df.iloc[0]['body']
        check_cell = '<p id="100">I agree fully with Lady Hale.</p>'
        assert cell == check_cell

    def test_remove_new_judge_line(self):
        data = [['------------- NEW JUDGE ---------------'], ['LORD SLYNN']]
        df = pd.DataFrame(data, columns=['body'])  
        length_check = 1
        df = app.fd.remove_new_judge_line(df)  
        length = len(df)
        assert length_check == length  
    
    def test_capitalize_doube_barrelled(self):
        judge = "browne-wilkinson" 
        judge = app.fd.capitalize_double_barrelled(judge)
        test_judge = "Browne-Wilkinson" 
        assert judge == test_judge

    def test_remove_duplicate_sentences(self):
        data = [['I disagree', '1'], ['I disagree', '1']]
        df = pd.DataFrame(data, columns=['body', 'line_col'])  
        df = app.fd.remove_duplicate_sentences(df)
        length = len(df)
        check_length = 1
        assert length == check_length
    
    def test_remove_title(self):
        judge = 'lord steyn'
        judge = app.fd.remove_title(judge)
        judge_check = 'steyn'
        assert judge_check == judge 

    def test_remove_title2(self):
        judge = 'self'
        judge = app.fd.remove_title(judge)
        check_judge = 'self'
        assert check_judge == judge 
    
    def test_get_data(self):
        data = [['partagr', 'lord steyn', 'lord hoffmann']]
        df = pd.DataFrame(data, columns=['relation_col', 'from_col', 'to_col'])  
        row = df.iloc[0]
        data = app.fd.get_data(row)
        data_check = 'partagr steyn hoffmann'
        assert data == data_check
    
    def test_check_relation(self):
        rel = 'fulldisa'
        return_value = app.fd.check_relation(rel)
        assert return_value == True
    
    def test_gather_tags(df):
        data = [['lady hale', 'lord steyn', 'partagr', '1'], ['lady hale', 'lord brown', 'fullagr', '1']]
        df = pd.DataFrame(data, columns=['from_col', 'to_col', 'relation_col', 'line_col'])  
        df = app.fd.gather_tags(df)
        cell = df.iloc[1]['relation_col']
        cell_check = ['partagr hale steyn', 'fullagr hale brown']
        assert cell == cell_check
    
    def test_make_full_sentence(self):
        sentence_check = 'full agreement from Steyn to Hale'
        rel = 'fullagr'
        text = 'steyn hale'
        sentence = app.fd.make_full_sentence(rel, text)
        assert sentence_check == sentence
    
    def test_make_full_sentence2(self):
        sentence_check = 'partial agreement from Steyn to Hale'
        rel = 'partagr'
        text = 'steyn hale'
        sentence = app.fd.make_full_sentence(rel, text)
        assert sentence_check == sentence
    
    def test_make_full_sentence3(self):
        sentence_check = 'full disagreement from Browne-Wilkinson to Brown'
        rel = 'fulldisa'
        text = 'browne-wilkinson brown'
        sentence = app.fd.make_full_sentence(rel, text)
        assert sentence_check == sentence

    def test_join_title(self):
        title_check = 'acknowledgment of Hoffmann by Hope, acknowledgment of Hobhouse by Hope'
        title = ['acknowledgment of Hoffmann by Hope', 'acknowledgment of Hobhouse by Hope']
        title = app.fd.join_title(title) 
        assert  title_check == title
    
    def test_get_rel_type(self):
        text = 'fullagr'
        result = app.fd.get_rel_type(text)
        assert result == 'fullagr'
    
    def test_get_rel_type2(self):
        text = 'ackn'
        result = app.fd.get_rel_type(text)
        assert result == 'ackn'
    
    def test_get_rel_type3(self):
        text = 'partdisa'
        result = app.fd.get_rel_type(text)
        assert result == 'partdisa'

    def test_replace_relation(self): 
        check = "<td class=\"fullagr-highlight\"> <div title=\"blank_title\"> Full agreement </div> </td> \n"
        item = 'fullagr'
        result = app.fd.replace_relation(item)
        assert check == result
    
    def test_replace_relation2(self): 
        check = "<td class=\"partagr-highlight\"> <div title=\"blank_title\"> Partial agreement </div>  </td> \n"
        item = 'partagr'
        result = app.fd.replace_relation(item)
        assert check == result
    
    def test_replace_relation3(self): 
        check = "<td class=\"outcome-highlight\"> <div title=\"blank_title\"> Outcome </div> </td> \n"
        item = 'outcome'
        result = app.fd.replace_relation(item)
        assert check == result
    
    def test_add_fullagr_to_dict(self):
        app.c.dictionary['100'] = {}
        line_col = '100' 
        data = 'hope hoffmann' 
        app.fd.add_fullagr_to_dict(line_col, data)
        check = ['hope hoffmann']
        assert app.c.dictionary['100']['fullagr'] == check 
    
    def test_add_partagr_to_dict(self):
        app.c.dictionary['7'] = {}
        line_col = '7' 
        data = 'hope hoffmann' 
        app.fd.add_partagr_to_dict(line_col, data)
        check = ['hope hoffmann']
        assert app.c.dictionary['7']['partagr'] == check 
    
    def test_add_fulldisa_to_dict(self):
        app.c.dictionary['2'] = {}
        line_col = '2' 
        data = 'hale hoffmann' 
        app.fd.add_fulldisa_to_dict(line_col, data)
        check = ['hale hoffmann']
        assert app.c.dictionary['2']['fulldisa'] == check 
    
    def test_add_outcome_to_dict(self):
        app.c.dictionary['201'] = {}
        line_col = '201' 
        data = 'hale slynn' 
        app.fd.add_outcome_to_dict(line_col, data)
        check = ['hale slynn']
        assert app.c.dictionary['201']['outcome'] == check 

class TestMetadataScraper(unittest.TestCase):
    def test_highlight_all_rels(self):
        data = [['LORD BROWNE-WILKINSON'], ['My lords, I am here today to say...']]
        df = pd.DataFrame(data, columns=['body'])
        df = app.fd.add_heading_tags(df)
        row = df.iloc[0]
        colour = app.ms.highlight_all_rels(row)
        colour_test = ['background-color: ' for r in row]
        assert colour == colour_test

    def test_format_case_text(self):
        app.ms.line_arr = ['2']
        data = [['LORD BROWNE-WILKINSON', '1'], ['My lords, I am here today to say...', '2']]
        df = pd.DataFrame(data, columns=['body', 'line_col'])
        df = app.ms.format_case_text(df)
        row = df.iloc[1]['body']
        row_check = "<a id=\"aaa2\">My lords, I am here today to say...</a>"
        assert row_check == row
    
    def test_make_full_disa(self):
        from_j = 'lady hale'
        to_j = 'lord steyn'
        line_col = '7'
        line_check =  '<br/> <br/>LADY HALE fully disagreed with LORD STEYN<a href=\"#aaa7\"  onclick="highlightLinks(href);"> [7] </a>\n\n\n\n'
        line = app.ms.make_full_disa(from_j, to_j, line_col)
        assert  line_check == line
    
    def test_make_part_disa(self):
        from_j = 'lady hale'
        to_j = 'lord steyn'
        line_col = '102'
        line_check =  '<br/> <br/>LADY HALE partially disagreed with LORD STEYN<a href=\"#aaa102\"  onclick="highlightLinks(href);"> [102] </a>\n\n\n\n'
        line = app.ms.make_part_disa(from_j, to_j, line_col)
        assert  line_check == line
    
    def test_make_disa(self):
        relation = 'fulldisa'
        from_j = 'lord browne-wilkinson'
        to_j = 'all'
        line_col = '103'
        line_check = '<br/> <br/>LORD BROWNE-WILKINSON fully disagreed with all<a href=\"#aaa103\"  onclick=\"highlightLinks(href);\"> [103] </a>\n\n\n\n'
        line = app.ms.make_disa(relation, from_j, to_j, line_col)
        assert line_check == line

    def test_add_disagreements(self):
        content = []
        content.append('Lord Hoffmann partially disagrees with Lord Steyn')
        content.append('<\br>')
        data = [['fulldisa', 'lord brown', 'lady hale', '111']]
        df = pd.DataFrame(data, columns=['relation_col', 'from_col', 'to_col', 'line_col'])
        content = app.ms.add_disagrements(content, df)
        line = content[1]
        line_check = '<br/> <br/>LORD BROWN fully disagreed with LADY HALE<a href=\"#aaa111\"  onclick="highlightLinks(href);"> [111] </a>\n\n\n\n'
        assert line == line_check
    
    def test_match_align_to_sentence(self):
        content = []
        content.append('Lord Hoffmann partially disagrees with Lord Steyn')
        content.append('<\br>') 
        data = [['1', '5', 'this is a test']]
        df_new = pd.DataFrame(data, columns=['align', 'asmo_sent_id', 'case_text'])
        content = app.ms.match_align_to_sentence(content, df_new)
        content_check = "Lord Hoffmann partially disagrees with Lord Steyn<a href=\"#aaa5\" onclick=\"highlightLinks(href);\"> [5] </a>"
        assert  content[0] == content_check      


class TestMakeGraphsAndSummary(unittest.TestCase):
    def setUp(self):
        sqlEngine = create_engine('mysql+pymysql://root:@127.0.0.1/all_data', pool_recycle=3600)
        dbConnection = sqlEngine.connect()

    def test_make_full_disa_mgs(self):
        from_j = 'lord steyn'
        to_j = 'lord brown'
        line = app.mgs.make_full_disa(from_j, to_j, '5')
        line_check = '<br/> <br/>LORD STEYN fully disagreed with LORD BROWN\n\n\n\n'
        assert line == line_check
    
    def test_make_part_disa_mgs(self):
        from_j = 'lord steyn'
        to_j = 'lord brown'
        line = app.mgs.make_part_disa(from_j, to_j, '5')
        line_check = '<br/> <br/>LORD STEYN partially disagreed with LORD BROWN\n\n\n\n'
        assert line == line_check
    
    def test_make_disa_mgs(self):
        rel = 'fulldisa'
        from_j = 'lord steyn'
        to_j = 'lord brown'
        line_col = '5'
        line = app.mgs.make_disa(rel, from_j, to_j, line_col)
        line_check = '<br/> <br/>LORD STEYN fully disagreed with LORD BROWN\n\n\n\n'
        assert line == line_check
    
    def test_make_disa_mgs2(self):
        rel = 'partdisa'
        from_j = 'lord steyn'
        to_j = 'lord brown'
        line_col = '6'
        line = app.mgs.make_disa(rel, from_j, to_j, line_col)
        line_check = '<br/> <br/>LORD STEYN partially disagreed with LORD BROWN\n\n\n\n'
        assert line == line_check

    def test_add_disagreemeents_mgs(self): 
        content = ['LADY HALE said she is unhappy with the outcome.', '\n']
        data = [['fulldisa', 'lord steyn', 'lady hale', '1007']]
        df = pd.DataFrame(data, columns=['relation_col', 'from_col', 'to_col', 'line_col'])
        content = app.mgs.add_disagrements(content, df)
        test_content = ['LADY HALE said she is unhappy with the outcome.', '<br/> <br/>LORD STEYN fully disagreed with LADY HALE\n\n\n\n', '\n']
        assert content == test_content
    
    def test_add_disagreemeents_mgs2(self): 
        content = ['LADY HALE said she is unhappy with the outcome.', '\n']
        data = [['partdisa', 'lord steyn', 'lady hale', '1007']]
        df = pd.DataFrame(data, columns=['relation_col', 'from_col', 'to_col', 'line_col'])
        content = app.mgs.add_disagrements(content, df)
        test_content = ['LADY HALE said she is unhappy with the outcome.', '<br/> <br/>LORD STEYN partially disagreed with LADY HALE\n\n\n\n', '\n']
        assert content == test_content
    
    def test_match_align_to_sentence(self):
        content = ['LORD MILLETT agreed with Lord Steyn']
        data = [['I fully agree with Lord Steyn.', '173', '1']]
        df_new = pd.DataFrame(data, columns=['case_text', 'asmo_sent_id', 'align'])
        content = app.mgs.match_align_to_sentence(content, df_new)
        content_check = ["<a id=\"bbb173\">LORD MILLETT agreed with Lord Steyn</a>"]
        assert content == content_check

    def test_find_date_match(self):
        date_check = '25 October 2001'
        date_match = app.mgs.find_date_match(date_check)
        assert date_match == ['25', 'october', '2001']
    
    def test_find_file_match(self):
        date_match = ['25', 'october', '2001']
        name_check = 'delaware'
        filename = app.mgs.find_file_match(date_match, name_check)
        assert filename == '25_october_2001_delaware.htm'
    
    def test_edit_map_file_numbers(self):
        map_file = 'example example example alt="123"'
        new_map_file = app.mgs.edit_map_file_numbers(map_file)
        map_file_check = 'example example example alt="bbb123"\n'
        assert new_map_file == map_file_check
    
    def test_edit_map_file_numbers2(self):
        map_file = 'example example example href="#partagr_steyn_slynn" alt=""'
        new_map_file = app.mgs.edit_map_file_numbers(map_file)
        map_file_check = 'example example example href="#bbbpartagr_steyn_slynn" alt=""\n'
        assert new_map_file == map_file_check

class TestMakeTabs(unittest.TestCase):
    # def test_make_content(self):
    #     f = open("static/partagr_hope_steyn.map", "w")
    #     line_check = '<div id="partagr_hope_steyn" class="tabcontent">\n\'\n \'<h6> This arrow represents multiple arrows: </h6>\n\'\n \'<img src=\"/static/partagr_hope_steyn.png" usemap="#partagr_hope_steyn"/>\n\'\n \'</div>\n\''
    #     name = "partagr_hope_steyn" 
    #     line = app.mt.make_content(name)
    #     assert line_check == line

    def test_make_button(self):
        line_check = '<button class="tablinks" onclick="openTab(event, \'partagr_hope_steyn\')"></button>\n'
        name = "partagr_hope_steyn" 
        line = app.mt.make_button(name)
        assert line_check == line

    def test_check_mo(self):
        test_line = 'irvine [shape="circle", fixedsize="true", height=1, width=1, style="filled", fillcolor="yellow", href="#irvine"];'
        check_mo = ['irvine']
        assert app.check_mo(test_line) == check_mo

    def test_check_mo(self):
        test_line = 'bingham [shape="circle", fixedsize="true", height=1, width=1, style="filled", fillcolor="white", href="#irvine"];'
        check_mo = []
        assert app.check_mo(test_line) == check_mo

    def test_get_case_name(self):
        long_name = 'Case 6 : Example Case'
        comparison = 'case6'
        assert app.get_case_name(long_name) == comparison

    def test_check_mo(self):
        line =  '"scott" [shape="circle", fixedsize="true", height=1, width=1, style="filled", fillcolor="yellow", href="#scott"];'
        comp_mo_judges = ['"scott"']
        assert app.check_mo(line) == comp_mo_judges

    def test_check_mo2(self):
        line =  '"scott" [shape="circle", fixedsize="true", height=1, width=1, style="filled", fillcolor="white", href="#scott"];'
        comp_mo_judges = [] 
        assert app.check_mo(line) == comp_mo_judges

    def test_make_partagr_edge(self):
        judge = {'to': 'lord hoffmann', 'from':'lady hale', 'line_number':123}
        line = '"hoffmann" -> { "hale" } [color="darkgreen", arrowhead="onormal", penwidth=1, href=\"123\"];\n'


class TestMakeMiniGraphs(unittest.TestCase):
    def test_strip_title(self):
        judge ="lady hale"
        judge_check = '"hale"'
        judge = app.mm.strip_title(judge)
        assert judge == judge_check

    def test_make_fullagr_edge(self):
        data = ['fullagr', 'hope', 'steyn']
        val = '83'
        line = app.mm.make_fullagr_edge(data, val)
        line_check = ' "hope" -> { "steyn" } [color="darkgreen", arrowhead="normal", penwidth=1, href="#83"]; \n'
        assert line == line_check
    
    def test_make_partagr_edge(self):
        data = ['partagr', 'brown', 'slynn']
        val = '83'
        line = app.mm.make_partagr_edge(data, val)
        line_check = ' "brown" -> { "slynn" } [color="darkgreen", arrowhead="onormal", penwidth=1, href="#83"]; \n'
        assert line == line_check

    def test_make_fulldis_edge(self):
        data = ['fulldisa', 'brown', 'slynn']
        val = '702'
        line = app.mm.make_fulldis_edge(data, val)
        line_check = ' "brown" -> { "slynn" } [color="red", arrowhead="dot", penwidth=1, href="#702"]; \n'
        assert line == line_check
    
    def test_make_partdis_edge(self):
        data = ['partdisa', 'brown', 'slynn']
        val = '702'
        line = app.mm.make_partdis_edge(data, val)
        line_check = ' "brown" -> { "slynn" } [color="red", arrowhead="odot", penwidth=1, href="#702"]; \n'
        assert line == line_check
    
    def test_make_outcome_edge(self):
        data = ['outcome', 'brown', 'slynn']
        val = '702'
        line = app.mm.make_outcome_edge(data, val)
        line_check = ' "brown" -> { "slynn" } [color="blue", arrowhead="vee", penwidth=1, href="#702"]; \n'
        assert line == line_check

    def test_whole_edge_function(self):
        data = ['outcome', 'brown', 'slynn']
        val = '702'
        line = app.mm.add_edge(data, val)
        line_check = ' "brown" -> { "slynn" } [color="blue", arrowhead="vee", penwidth=1, href="#702"]; \n'
        assert line == line_check
    
    def test_whole_edge_function2(self):
        data = ['partagr', 'brown', 'slynn']
        val = '83'
        line = app.mm.add_edge(data, val)
        line_check = ' "brown" -> { "slynn" } [color="darkgreen", arrowhead="onormal", penwidth=1, href="#83"]; \n'
        assert line == line_check

    def test_trim_judge_mm(self):
        name = 'lord slynn'
        name_check = 'slynn'
        name = app.mm.trim_judge(name) 
        assert name == name_check 
    
    def test_make_judge_collections(self):
        judge_dict = [{'from': 'lord nicholls', 'to': 'lord hoffmann', 'relation': 'fullagr', 'line_number': '6'}, {'from': 'lord nicholls', 'to': 'self', 'relation': 'outcome', 'line_number': '6'}, {'from': 'lord hoffmann', 'to': 'self', 'relation': 'outcome', 'line_number': '236'}, {'from': 'lord hope', 'to': 'lord hoffmann', 'relation': 'fullagr', 'line_number': '242'}, {'from': 'lord hope', 'to': 'lord hobhouse', 'relation': 'fullagr', 'line_number': '242'}, {'from': 'lord hope', 'to': 'self', 'relation': 'outcome', 'line_number': '242'}, {'from': 'lord hobhouse', 'to': 'self', 'relation': 'outcome', 'line_number': '247'}, {'from': 'lord hobhouse', 'to': 'lord hoffmann', 'relation': 'fullagr', 'line_number': '248'}, {'from': 'lord hobhouse', 'to': 'lord hoffmann', 'relation': 'partagr', 'line_number': '276'}, {'from': 'lord hobhouse', 'to': 'lord hoffmann', 'relation': 'partagr', 'line_number': '287'}, {'from': 'lord hobhouse', 'to': 'lord hoffmann', 'relation': 'partagr', 'line_number': '288'}, {'from': 'lord scott', 'to': 'lord hoffmann', 'relation': 'fullagr', 'line_number': '295'}, {'from': 'lord scott', 'to': 'self', 'relation': 'outcome', 'line_number': '295'}]
        all_judges = ['nicholls', 'hoffmann', 'hope', 'hobhouse', 'scott']
        result = app.mm.make_judge_collections(judge_dict, all_judges)
        result_check = {'fullagr_nicholls_hoffmann': ['6'], 'outcome_nicholls_self': ['6'], 'outcome_hoffmann_self': ['236'], 'fullagr_hope_hoffmann': ['242'], 'fullagr_hope_hobhouse': ['242'], 'outcome_hope_self': ['242'], 'outcome_hobhouse_self': ['247'], 'fullagr_hobhouse_hoffmann': ['248'], 'partagr_hobhouse_hoffmann': ['276', '287', '288'], 'fullagr_scott_hoffmann': ['295'], 'outcome_scott_self': ['295']}
        assert result == result_check
    
    def test_make_judge_collections2(self):
        judge_dict = [{'from': 'lord steyn', 'to': 'lord cooke', 'relation': 'fullagr', 'line_number': '7'}, {'from': 'lord steyn', 'to': 'self', 'relation': 'outcome', 'line_number': '7'}, {'from': 'lord browne-wilkinson', 'to': 'lord cooke', 'relation': 'fullagr', 'line_number': '13'}, {'from': 'lord browne-wilkinson', 'to': 'self', 'relation': 'outcome', 'line_number': '13'}, {'from': 'lord cooke', 'to': 'self', 'relation': 'outcome', 'line_number': '283'}, {'from': 'lord clyde', 'to': 'lord cooke', 'relation': 'fullagr', 'line_number': '289'}, {'from': 'lord clyde', 'to': 'self', 'relation': 'outcome', 'line_number': '289'}, {'from': 'lord hutton', 'to': 'lord cooke', 'relation': 'fullagr', 'line_number': '295'}, {'from': 'lord hutton', 'to': 'self', 'relation': 'outcome', 'line_number': '295'}]
        all_judges = ['steyn', 'browne-wilkinson', 'cooke', 'clyde', 'hutton']
        result = app.mm.make_judge_collections(judge_dict, all_judges)
        result_check = {'fullagr_steyn_cooke': ['7'], 'outcome_steyn_self': ['7'], 'fullagr_browne-wilkinson_cooke': ['13'], 'outcome_browne-wilkinson_self': ['13'], 'outcome_cooke_self': ['283'], 'fullagr_clyde_cooke': ['289'], 'outcome_clyde_self': ['289'], 'fullagr_hutton_cooke': ['295'], 'outcome_hutton_self': ['295']}
        assert result == result_check
    
    def test_make_nodes(self):
        dot_file = ' K=0.6 \n "rodger" -> { "millett" } [color="darkgreen", arrowhead="onormal", penwidth=1, href="#254"]; \n "rodger" -> { "millett" } [color="darkgreen", arrowhead="onormal", penwidth=1, href="#265"];'
        data = ['partagr', 'rodger', 'millett']
        values = ['254', '265']
        dot_file_check = ' K=0.6 \n "rodger" -> { "millett" } [color="darkgreen", arrowhead="onormal", penwidth=1, href="#254"]; \n "rodger" -> { "millett" } [color="darkgreen", arrowhead="onormal", penwidth=1, href="#265"]; "rodger" [shape="circle", fixedsize="true", height=1, width=1, style="filled", fillcolor="white", href="#rodger"]; \n "millett" [shape="circle", fixedsize="true", height=1, width=1, style="filled", fillcolor="white", href="#millett"]; \n'
        dot_file = app.mm.make_nodes(dot_file, data, values)
        assert dot_file == dot_file_check

class TestHardClass(unittest.TestCase):
    def setUp(self):
        app.c.mo_judges = ['steyn', 'hale', 'mance']
        app.judges = ['"hale"', '"brown"']
        app.selected_roles_list = ['framing', 'fact']

    def test_maj_op(self):
        test_sentence = 'The majority opinion is given by Steyn, Hale and Mance.'
        assert app.find_mo_judges() == test_sentence
    
    def test_check_judge(self):
        line = '"bingham" [shape="circle", fixedsize="true", height=1, width=1, style="filled", fillcolor="white", href="#bingham"];'
        comparison_judges = ['"hale"', '"brown"', '"bingham"']
        app.check_judge(line)
        assert app.judges == comparison_judges
