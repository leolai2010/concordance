import pandas as pd
import datetime
from collections import defaultdict

files = []
outputFileName = datetime.date.today().strftime('%Y%m%d') + '_' + datetime.datetime.now().strftime('%H%M%S')
outputFilePath = ""

def removeDuplicates(result):
    dropResult = set()
    dropResult_add = dropResult.add
    resultDrop = [drop for drop in result if not (drop in dropResult or dropResult_add(drop))]
    return resultDrop

def inputCleanUp(data, input_type):
    output_list = []
    if input_type == 'sample':
        for name in data:
            output_list.append(name[:3])
        return output_list
    elif input_type == 'marker':
        for marker in data:
            marker = str(marker).replace(" ", "").upper()
            if marker == 'RS199815934':
                output_list.append('YINDEL')
            else:
                output_list.append(marker)
        return output_list

def obtainValuesFromTable(column, type):
    output_list = []
    if type == '*':
        for values in files:
            output_list.extend(removeDuplicates(pd.read_csv(values).iloc[:,column].to_list()))
    else:
        output_list.extend(removeDuplicates(pd.read_csv(type).iloc[:,column].to_list()))
    output_list = removeDuplicates(output_list)
    return output_list

def formatInputFiles():
    output_list = []
    for file in files:
        df = pd.read_csv(file)
        df_cleanSample = inputCleanUp(df.iloc[:,0], 'sample')
        df_cleanMarker = inputCleanUp(df.iloc[:,1], 'marker')
        df['Sample File'] = df_cleanSample
        df['Marker'] = df_cleanMarker
        output_list.append(df)
    return output_list

def alleleCleanUp(alleles):
    if alleles == 'NaN,NaN':
        return 'None'
    else:
        separate = str(alleles).split(',')
        for allele in separate:
            if allele == 'NaN':
                separate.remove(allele)
        allele = ','.join(separate)
        return allele

def format(fileDrop):
    data_frames = formatInputFiles()
    sample_list = sorted(inputCleanUp(obtainValuesFromTable(0, '*'), 'sample'))
    marker_list = removeDuplicates(inputCleanUp(obtainValuesFromTable(1, '*'), 'marker'))
    concensus_dic = {}
    for sample in sample_list:
        max_marker = {}
        for marker in marker_list: 
            allele_read = defaultdict(str)
            for df in data_frames:
                matching = df.loc[(df.iloc[:,0] == sample) & (df.iloc[:,1] == marker)]
                if matching.empty == True:
                    first_allele, second_allele = 'NaN', 'NaN'
                else:
                    first_allele, second_allele = matching.iloc[:,3], matching.iloc[:,4]
                    if first_allele.empty != True:
                        first_allele = first_allele.to_string(index=False)
                    if second_allele.empty != True:
                        second_allele = second_allele.to_string(index=False)
                allele = first_allele+','+second_allele
                allele = alleleCleanUp(allele)
                allele_read.setdefault(allele, 0)
                allele_read[allele] += 11
            if len(allele_read) > 1 and 'None' in allele_read.keys():
                del allele_read['None']
            max_marker[marker] = max(allele_read, key=allele_read.get)
        concensus_dic[sample] = max_marker
    result = pd.DataFrame.from_dict(concensus_dic, orient='index')
    if fileDrop == True:
        result.to_excel(outputFilePath)
    return result

referenceFile = ''
def concordance(fileDrop, onlyMismatch):
    referenceDf = pd.read_excel(referenceFile)
    compareDf = pd.DataFrame(columns=['Sample', 'Match', 'Result Genotype', 'Reference Genotype'])
    formatDf = formatInputFiles()
    count = 0
    for file in files:
        fileName = file.rsplit('/', 1)[1][:-4]
        inputDf = formatDf[count]
        sample_list = inputCleanUp(obtainValuesFromTable(0, file), 'sample')
        marker_list = removeDuplicates(inputCleanUp(obtainValuesFromTable(1, file), 'marker'))
        for sample in sample_list:
            for marker in marker_list:
                matching = inputDf.loc[(inputDf.iloc[:,0] == sample) & (inputDf.iloc[:,1] == marker)]
                compare = referenceDf.loc[(referenceDf.iloc[:,0] == sample), marker].to_string(index=False)
                compare = alleleCleanUp(compare)
                if matching.empty == True:
                    first_allele, second_allele = 'NaN', 'NaN'
                else:
                    first_allele, second_allele = matching.iloc[:,3], matching.iloc[:,4]
                    if first_allele.empty != True:
                        first_allele = first_allele.to_string(index=False)
                    if second_allele.empty != True:
                        second_allele = second_allele.to_string(index=False)
                allele = first_allele+','+second_allele
                allele = alleleCleanUp(allele)
                if allele != compare:
                    matched = 'No'
                    compareDf = compareDf.append({'Sample':sample, 'Match':matched, 'Result Genotype':marker+' : '+allele, 'Reference Genotype':marker+' : '+compare}, ignore_index=True)
                else:
                    if onlyMismatch == False:
                        matched = 'Yes'
                        compareDf = compareDf.append({'Sample':sample, 'Match':matched, 'Result Genotype':marker+' : '+allele, 'Reference Genotype':marker+' : '+compare}, ignore_index=True)
        if(fileDrop == True):
            compareDf.to_excel(outputFilePath)
        count = count + 1
    return compareDf
concordance(True, True)