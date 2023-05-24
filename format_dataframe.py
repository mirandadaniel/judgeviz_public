import config as c

def remove_htm(df):
    df = df.iloc[1: , :]
    return df

def remove_new_judge_line(df):
    for i, row in df.iterrows():
        index = row.name
        value = row.loc['body']
        if('------------- NEW JUDGE ---------------' in value):
            df.drop([index], axis=0, inplace=True)
    return df

def add_heading_tags(df):
    for i, row in df.iterrows():
        index = row.name
        value = row.loc['body']
        for x in c.all_judges:
            x = x.strip('"')
            if('LORD' in value) and (x.upper() in value):
                value = '<p id="{}";>'.format(x) + '<b>' + value + '</b> </p>'
                df.at[index, 'body']=value
    return df

def add_html_tags(df):
    for i, row in df.iterrows():
        index = row.name
        label = row.loc['relation_col']
        value = row.loc['body']
        line_col = row.loc['line_col']
        if(label != None):
            if('ackn' in label or 'fullagr' in label or 'partagr' in label or 'fulldisa' in label or 'partdisa' in label or 'outcome' in label):
                new_value = '<p id="{}">'.format(line_col) + value + '</p>'
                df.at[index, 'body']=new_value
    return df


def capitalize_double_barrelled(judge):
    judge = judge.split('-')
    judge = judge[0].capitalize() + '-' + judge[1].capitalize()
    return judge



def format_fullagr(from_col, to, rel, body, prev_label, prev_judge_from):
    sentence = 'full agreement from ' + from_col + ' to ' + to
    if(prev_label != 'NAN' and prev_label != None and from_col == prev_judge_from):
        sentence = prev_label + ', ' + sentence
        return sentence
    else:
        from_col = capitalize_judge(from_col)
        to = capitalize_judge(to)
        sentence = 'Full agreement from ' + from_col + ' to ' + to
        return sentence
    
def format_partagr(from_col, to, rel, body, prev_label, prev_judge_from):
    sentence = 'partial agreement from ' + from_col + ' to ' + to
    if(prev_label != 'NAN') and (prev_label != None) and (from_col == prev_judge_from): 
        sentence = prev_label + ', ' + sentence
        return sentence
    else:
        sentence = sentence.capitalize()
        return sentence

def format_fulldis(from_col, to, rel, body, prev_label, prev_judge_from):
    sentence = 'full disagreement from ' + from_col + ' to ' + to
    if(prev_label != 'NAN') and (prev_label != None) and (from_col == prev_judge_from): 
        sentence = prev_label + ', ' + sentence
        return sentence
    else:
        sentence = sentence.capitalize()
        return sentence

def format_partdis(from_col, to, rel, body, prev_label, prev_judge_from):
    sentence = 'partial disagreement from ' + from_col + ' to ' + to
    if(prev_label != 'NAN') and (prev_label != None) and (from_col == prev_judge_from): 
        sentence = prev_label + ', ' + sentence
        return sentence
    else:
        sentence = sentence.capitalize()
        return sentence

def format_outcome(from_col, to, rel, body, prev_label, prev_judge_from):
    sentence = 'agreement on outcome from ' + from_col + ' to ' 
    if(prev_label != 'NAN') and (prev_label != None) and (from_col == prev_judge_from):    
        sentence = prev_label + ', ' + sentence + to
        return sentence
    else:
        sentence = 'Agreement on outcome from ' + from_col + ' to ' + to
        return sentence

def capitalize_judge(judge_name):
    if(' ' in judge_name):
        judge_name = judge_name.split(' ')
        length = len(judge_name)
        if(length == 2):
            judge_name[0] = judge_name[0].capitalize()
            judge_name[1] = judge_name[1].capitalize()
            if('-' in judge_name[1]):
                judge_name[1] = capitalize_double_barrelled(judge_name[1])
            judge_name = ' '.join(judge_name)
            return judge_name
    else:
        return judge_name


def format_sentence(from_col, to, rel, body, prev_label, prev_judge_from): 
    from_col = capitalize_judge(from_col)
    to = capitalize_judge(to)
    prev_judge_from = capitalize_judge(prev_judge_from)
    if(rel == 'outcome'):
        sentence = format_outcome(from_col, to, rel, body, prev_label, prev_judge_from)
        return sentence
    elif(rel == 'fullagr'):
        sentence = format_fullagr(from_col, to, rel, body, prev_label, prev_judge_from)
        return sentence
    elif(rel == 'partagr'):
        sentence = format_partagr(from_col, to, rel, body, prev_label, prev_judge_from)
        return sentence
    elif(rel == 'fulldisa'):
        sentence = format_fulldis(from_col, to, rel, body, prev_label, prev_judge_from)
        return sentence
    elif(rel == 'partdisa'):
        sentence = format_partdis(from_col, to, rel, body, prev_label, prev_judge_from)
        return sentence

def remove_duplicate_sentences(df):
    prev_line = ''
    for i, row in df.iterrows():
        curr_line = row.loc['line_col'].strip()
        index = row.name
        if(curr_line == prev_line):
            df.drop([index-1], axis=0, inplace=True)
            prev_line = curr_line
        prev_line = curr_line
    return df

def remove_title(judge):
    if(' ' in judge):
        judge = judge.split(' ')
        judge = judge[1]
    return judge

def get_data(row):
    judge_from = row.loc['from_col']
    judge_to = row.loc['to_col']
    relation = row.loc['relation_col']
    data = relation + ' ' + remove_title(judge_from) + ' ' + remove_title(judge_to)
    return data

def check_relation(rel):
    if('fullagr' in rel or 'partagr' in rel or 'fulldisa' in rel or 'partdisa' in rel or 'outcome' in rel or 'factagr' in rel or 'ackn' in rel):
        return True

def gather_tags(df):
    prev_label = ''
    prev_line = ''
    for i, row in df.iterrows():
        if(check_relation(row.loc['relation_col'])):
            index = row.name
            curr_data = [get_data(row)]
            df.at[index, 'relation_col']=curr_data
            curr_line = row.loc['line_col'] 
            if(curr_line == prev_line):
                prev_data = df.at[index-1, 'relation_col']
                data_list = []
                data_list.extend(prev_data)
                data_list.extend(curr_data)
                df.at[index, 'relation_col']= data_list
                prev_data = data_list 
        prev_label = row.loc['relation_col']
        prev_line = row.loc['line_col']
    return df


def make_full_sentence(rel, text):
    text = text.lstrip()
    text = text.split()
    if('-' in text[0]):
            judge1 = capitalize_double_barrelled(text[0])
    else:
        judge1 = text[0].capitalize()
    judge2 = text[1]
    if(judge2 != 'self' or judge2 != 'all'):
        if('-' in judge2):
            judge2 = capitalize_double_barrelled(judge2)
        else:
            judge2 = judge2.capitalize()
    if('fullagr' in rel):
        rel = 'full agreement from '
        text = rel + judge1 + " to " + judge2
        return text
    elif('partagr' in rel):
        rel = 'partial agreement from '
        text = rel + judge1 + " to " + judge2
        return text
    elif('fulldisa' in rel):
        rel = 'full disagreement from '
        text = rel + judge1 + " to " + judge2
        return text
    elif('partdisa' in rel):
        rel = 'partial disagreement from '
        text = rel + judge1 + " to " + judge2
        return text
    elif('outcome' in rel):
        rel = 'agreement on outcome from '
        text = rel + judge1 + " to " + judge2
        return text
    elif('ackn' in rel):
        rel = 'acknowledgment of '
        text = rel + judge2 + " by " + judge1
        return text
    elif('factagr' in rel):
        rel = 'agreement on facts from '
        text = rel + judge1 + " to " + judge2
        return text

def get_title(line_col, rel_type):
    rel_text = c.dictionary[line_col][rel_type]
    return rel_text

def join_title(title):
    title = ', '.join(title)
    return title

def format_title(rel, title):
    new_title = []
    for x in title:
        x = make_full_sentence(rel, x)
        new_title.append(x)
    return new_title

def get_rel_type(text):
    if('fullagr' in text):
        return 'fullagr'
    if('partagr' in text):
        return 'partagr'
    if('fulldisa' in text):
        return 'fulldisa'
    if('partdisa' in text):
        return 'partdisa'
    if('outcome' in text):
        return 'outcome'
    if('ackn' in text):
        return 'ackn'
    if('factagr' in text):
        return 'factagr'
    
def replace_title(df):
    for i, row in df.iterrows():
        index = row.name
        line_col = row.loc['line_col']
        text = row.loc['relation_col']
        if('NAN' not in text):
            substr = "<td class="
            count = text.count(substr)
            if(count == 1):
                rel = get_rel_type(text)
                title = get_title(line_col, rel)
                title = format_title(rel, title)
                title = join_title(title)
                title = title
                data = text.replace('blank_title', title)
                df.at[index, 'relation_col']= data
            elif(count > 1):
                text = text.split('</td>')
                full_line = ''
                for x in text:
                    if "</table>" not in x:
                        rel = get_rel_type(x)
                        title = get_title(line_col, rel)
                        title = format_title(rel, title)
                        title = join_title(title)
                        data = x.replace('blank_title', title)
                        full_line = full_line + data
                    else:
                        full_line = full_line + x
                df.at[index, 'relation_col']= full_line
                
        else:
            df.at[index, 'relation_col']= ''
    return df

def replace_relation(item):
    if('fullagr' in item):
        item = "<td class=\"fullagr-highlight\"> <div title=\"blank_title\"> Full agreement </div> </td> \n"
        return item 
    if('partagr' in item):
        item = "<td class=\"partagr-highlight\"> <div title=\"blank_title\"> Partial agreement </div>  </td> \n"
        return item 
    if('fulldisa' in item):
        item = "<td class=\"fulldisa-highlight\"> <div title=\"blank_title\"> Full disagreement </div> </td> \n"
        return item 
    if('partdisa' in item):
        item = "<td class=\"partdisa-highlight\"> <div title=\"blank_title\"> Partial disagreement </div> </td> \n"
        return item 
    if('outcome' in item):
        item = "<td class=\"outcome-highlight\"> <div title=\"blank_title\"> Outcome </div> </td> \n"
        return item 
    if('ackn' in item):
        item = "<td class=\"ackn-highlight\"> <div title=\"blank_title\"> Acknowledgment </div> </td> \n"
        return item 
    if('factagr' in item):
        item = "<td class=\"factagr-highlight\"> <div title=\"blank_title\"> Factual agreement </div> </td> \n"
        return item 

def split_item(item):
    item = item.split()
    rel = item[0]
    return rel

def add_fullagr_to_dict(line_col, data):
    data = data.replace('fullagr', '')
    if('fullagr' in c.dictionary[line_col]):
        data_arr = []
        data_arr.append(data)
        c.dictionary[line_col]['fullagr'].extend(data_arr)
    else:
        c.dictionary[line_col]['fullagr'] = [data]

def add_partagr_to_dict(line_col, data):
    data = data.replace('partagr', '')
    if('partagr' in c.dictionary[line_col]):
        data_arr = []
        data_arr.append(data)
        c.dictionary[line_col]['partagr'].extend(data_arr)
    else:
        c.dictionary[line_col]['partagr'] = [data]


def add_fulldisa_to_dict(line_col, data):
    data = data.replace('fulldisa', '')
    if('fulldisa' in c.dictionary[line_col]):
        data_arr = []
        data_arr.append(data)
        c.dictionary[line_col]['fulldisa'].extend(data_arr)
    else:
        c.dictionary[line_col]['fulldisa'] = [data]

def add_partdisa_to_dict(line_col, data):
    data = data.replace('partdisa', '')
    if('partdisa' in c.dictionary[line_col]):
        data_arr = []
        data_arr.append(data)
        c.dictionary[line_col]['partdisa'].extend(data_arr)
    else:
        c.dictionary[line_col]['partdisa'] = [data]

def add_outcome_to_dict(line_col, data):
    data = data.replace('outcome', '')
    if('outcome' in c.dictionary[line_col]):
        data_arr = []
        data_arr.append(data)
        c.dictionary[line_col]['outcome'].extend(data_arr)
    else:
        c.dictionary[line_col]['outcome'] = [data]

def add_factagr_to_dict(line_col, data):
    data = data.replace('factagr', '')
    if('factagr' in c.dictionary[line_col]):
        data_arr = []
        data_arr.append(data)
        c.dictionary[line_col]['factagr'].extend(data_arr)
    else:
        c.dictionary[line_col]['factagr'] = [data]

def add_ackn_to_dict(line_col, data):
    data = data.replace('ackn', '')
    if('ackn' in c.dictionary[line_col]):
        data_arr = []
        data_arr.append(data)
        c.dictionary[line_col]['ackn'].extend(data_arr)
    else:
        c.dictionary[line_col]['ackn'] = [data]

def assign_data(line_col, data):
    if('fullagr' in data):
        add_fullagr_to_dict(line_col, data)
    elif('partagr' in data):
        add_partagr_to_dict(line_col, data)
    elif('fulldisa' in data):
        add_fulldisa_to_dict(line_col, data)
    elif('partdisa' in data):
        add_partdisa_to_dict(line_col, data)
    elif('outcome' in data):
        add_outcome_to_dict(line_col, data)
    elif('factagr' in data):
        add_factagr_to_dict(line_col, data)
    elif('ackn' in data):
        add_ackn_to_dict(line_col, data)

def find_what_relation(line_col, data): 
    for x in data:
        x = x.split(',')
        if(len(x) > 1):
            for i in x:
                assign_data(line_col, i)
        else:
            assign_data(line_col, x[0])

def format_cells(df):
    prev_item = ''
    for i, row in df.iterrows():
        index = row.name
        line_col = row.loc['line_col']
        if('NAN' not in row.loc['relation_col']):
            table = " <table class=\"nested\"> \n "
            data = row.loc['relation_col']
            rel_list = []
            c.dictionary[line_col] = {}
            find_what_relation(line_col, data)
            for item in data:
                rel = split_item(item)
                if(rel not in rel_list):
                    row = replace_relation(item)
                    table = table + "<tr> \n " + row + " <tr> \n"
                    table = table 
                    rel_list.append(rel)
            table = table + "</table> "
            df.at[index, 'relation_col']= table 
    return df
      
def format_dataframe(df):
    df = add_heading_tags(df)
    df = remove_htm(df)
    df = remove_new_judge_line(df)
    df = add_html_tags(df)
    df = gather_tags(df)
    df = remove_duplicate_sentences(df)
    df = format_cells(df)
    df = replace_title(df)
    return df

def format_dataframe_summary_text(df):
    df = add_heading_tags(df)
    df = remove_htm(df)
    df = remove_new_judge_line(df)
    df = gather_tags(df)
    df = remove_duplicate_sentences(df)
    df = format_cells(df)
    df = replace_title(df)
    return df
