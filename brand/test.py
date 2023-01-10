def check_phonetically_sound(names:list):
    vowel = {'a','e','i','o','u'};
    score_word={}
    for name in names:
        count=0
        for x in range(0, len(name), 3):
            if any(char in vowel for char in name[x:x+3]):
                count+=1
        score_word[name]=count/len(name)

    score_word=list(dict(sorted(score_word.items(), key=lambda item: item[1],reverse=True)).keys())
    return score_word

print(check_phonetically_sound(('gosmfapsl','fsefsdedesds','jdsakdfs','skssasdnsdisdf','aeraeaf')))