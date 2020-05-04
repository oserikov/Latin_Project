import re

def opening_f(file_nam):
    with open('latindict.txt', encoding='utf-8') as f:
        data_1 = f.read().splitlines()
    data = []
    for elem in data_1:
        if re.search(r'[а-я]', elem):
            data.append(elem)
    return data

res_op = opening_f('latindict.txt')
#print(res_op)


def not_nouns(some_arr):  #фильтр избавляется от сущ.
    no_noun = []
    pattern_gen_symb = '([a-z]+ m)|([a-z]+ f)|([a-z]+ n)'
    for line in some_arr:
        if not re.search(pattern_gen_symb, line):
            no_noun.append(line)
    return no_noun

res1 = not_nouns(res_op)
#print(res1)

def not_verbs(some_arr):    #избавляется от глаг.
    not_nouns_and_verbs = []
    pattern_num = '\d'
    pattern_rus = '(ть$)|(ться$)'
    for line in some_arr:
        if not re.search(pattern_num, line):
            if not re.search(pattern_rus, line):
                not_nouns_and_verbs.append(line)
    return not_nouns_and_verbs

res2 = not_verbs(res1)
#print(res2)

def not_pronoun(some_arr):     #может, дополнить паттерн= этот, какой-то, какой и тд.    Избавляется от местоим.
    no_pron = []
    pattern_com = '(\w*, \w*, \w*)(    \w*, \w*, \w*)'
    for line in some_arr:
        if not re.findall(pattern_com, line):
            no_pron.append(line)
    return no_pron

res3 = not_pronoun(res2)
#print(res3)


def not_prepos(some_arr):     #избавляется от предлогов
    no_prepos = []
    pattern_caus = "(\+)(NOM)|(GEN)|(ACC)|(DAT)|(ABL)"
    for line in some_arr:
        if not re.search(pattern_caus, line):
            no_prepos.append(line)
    return no_prepos

res4 = not_prepos(res3)
#print(res4)

def separate_forms(some_arr):      #отделяет 3 формы и перевод
    adj_forms = []
    translation = []
    for line in some_arr:
        forms, trans = line.split('    ')
        translation.append(trans)
        form = forms.split(', ')
        adj_forms.append(form)
    di_slot = [[x,y] for x, y in zip(adj_forms, translation)]
    return di_slot

res5 = separate_forms(res4)
#print(res5)

def choose_adj(some_arr):
    adj_only = []
    for f_arr in some_arr:
        trans = f_arr[1]
        if trans.endswith('й'):
            adj_only.append(f_arr)
    return adj_only

res100 = choose_adj(res5)
#print(res100)


def user(some_arr):

    print('Введите прилагательное в 1 форме (m, Nom, Sg)')
    serching_word = input()
    while len(serching_word) < 2:
        print('Почему вы решили ничего не напечатать? Хотите об этом поговорить?', '\nКак насчет ввести слово?')
        serching_word = input()

    exist_words = []
    for f_arr in some_arr:
        m_adj = (f_arr[0][0])
        exist_words.append(m_adj)
    while serching_word not in exist_words:
        print('Вы ввели слово:', serching_word)
        print('Извините, этого слова нет в нашем словаре. Попробуйте другое')
        serching_word = input()
    print('Вы ввели слово:', serching_word)
    return serching_word

res200 = user(res100)


def fill_1_2_declin(some_arr):     #дописывает формы до полных у 1 и 2 скл.
    for f_arr in some_arr:
        form = f_arr[0]
        if len(form) == 3 and form[1] == 'a' and form[2] == 'um':
            form[1] = form[0].replace('us', 'a')
            form[2] = form[0].replace('us', 'um')
            continue
    return some_arr

res6 = fill_1_2_declin(res100)
#print(res6)

def fill_3_declin_for_1end(some_arr):  #дописывает формы у 3 скл, у прил. одного окончания
    arr_gen = []
    forms_0 = []
    transes = []
    for f_arr in some_arr:
        translation = (f_arr[1])
        form = (f_arr[0])
        if form[1].startswith("gen: "):
            forms_0.append(form[0])
            transes.append(translation)
            gen_f = form[1].replace("gen: ", " ")
            arr_gen.append([gen_f, translation])
    third_dec_1end = [[[x, y], z] for x, y, z in zip(forms_0, forms_0, transes)]
    return some_arr, third_dec_1end, arr_gen

res7, res18, res19 = fill_3_declin_for_1end(res6)
#print(res7,"\n\n", res18, "\n\n", res19)
#print("Слова 3скл, одного оконч.:", res18)

def fill_3_declin_for_sim_end_2_3(some_arr):   #дописывает формы у 3 скл, у прил. двух и трех окончаний
    end2 = []
    end3 = []

    for f_arr in some_arr:
        trois1 = []
        forms = f_arr[0]
        translation = f_arr[1]
        if len(forms) == 2 and not forms[1].startswith('gen: '):
            trois1.extend([forms[0], forms[0], forms[1]])
            end2.append([trois1, translation])
        if len(forms) == 3 and forms[0] != forms[1] and not forms[1].endswith("a") and not forms[2].endswith("um"):
            trois2 = []
            trois2.extend([forms[0], forms[1], forms[2]])
            end3.append([[forms[0], forms[1], forms[2]], translation])

    return some_arr, end2, end3

res8, res20, res24 = fill_3_declin_for_sim_end_2_3(res7)
#print(res8, "\n\n", "прил.2оконч.:", res20, "\n\n", res24)

def only_decl_1_2(some_arr):     #массив прил. только 1 и 2 скл.
    declin_1_2 = []
    for f_arr in some_arr:
        forms = f_arr[0]
        translation = f_arr[1]
        if len(forms) == 3 and forms[1].endswith('a') and forms[2].endswith('um'):
            m = (forms[0])
            f = (forms[1])
            n = (forms[2])
            declin_1_2.append([[m, f, n], translation])

    return declin_1_2

res9 = only_decl_1_2(res8)
#print(res9)


def making_forms_1(some_arr):
    femin_Sg = []
    femin_Sg_end = ["a", "ae", "ae", "am", "a"]      #[Nom, Gen, Dat, Acc, Abl]
    exc = ["liber", "miser", "asper", "tener"]
    for f_arr in some_arr:
        caus_fem_Sg = []
        forms = f_arr[0]
        translation = f_arr[1]
        fem_trans = (translation[:-2] + 'ая')
        f = (forms[1][:-1])
        pattern_er = (forms[0])
        for caus_end in femin_Sg_end:
            if pattern_er.endswith('er'):
                if pattern_er in exc:
                    caus_f = (f + caus_end)
                else:
                    string = pattern_er[::-1]
                    f = (string.replace('re', 'r', 1))[::-1]
                    caus_f = (f + caus_end)
            else:
                caus_f = (f + caus_end)
            caus_fem_Sg.append(caus_f)
        femin_Sg.append([caus_fem_Sg, fem_trans])

    femin_Pl = []
    femin_Pl_end = ["ae", "arum", "is", "as", "is"]  # [Nom, Gen, Dat, Acc, Abl]
    for f_arr in some_arr:
        caus_fem_Pl = []
        forms = f_arr[0]
        translation = f_arr[1]
        fem_trans = (translation[:-2] + 'ые')
        f = (forms[1][:-1])
        pattern_er = (forms[0])
        for caus_end in femin_Pl_end:
            if pattern_er.endswith('er'):
                if pattern_er in exc:
                    caus_f = (f + caus_end)
                else:
                    string = pattern_er[::-1]
                    f = (string.replace('re', 'r', 1))[::-1]
                    caus_f = (f + caus_end)
            else:
                caus_f = (f + caus_end)
            caus_fem_Pl.append(caus_f)
        femin_Pl.append([caus_fem_Pl, fem_trans])
    return femin_Sg, femin_Pl

res10, res11 = making_forms_1(res9)
#print("Парадигма склонения прил. ж.р. ед.ч.:", res10, "\n\n\n", "Парадигма склонения прил. ж.р. мн.ч.:", res11, "\n\n")

def making_forms_2_m(some_arr):
    musc_Sg = []
    musc_Sg_end = ["us", "i", "o", "um", "o"] #обычные
    musc_Sg_end_ex = ["", "i", "o", "um", "o"]
    musc_Sg_end_er = ["er", "ri", "ro", "rum", "ro"]  #для слов с -er
    exc = ["liber", "miser", "asper", "tener"]  #искл. на -er
    for f_arr in some_arr:
        caus_musc_Sg = []
        forms = f_arr[0]
        translation = f_arr[1]
        musc_trans = (translation[:-2] + 'ый')
        f = (forms[1][:-1])
        pattern_er = (forms[0])
        for caus_end in musc_Sg_end_ex:
            if pattern_er.endswith('er'):
                if pattern_er in exc:
                    caus_m = f + caus_end
                    caus_musc_Sg.append(caus_m)
        for er_ends in musc_Sg_end_er:
            if pattern_er.endswith('er'):
                if pattern_er not in exc:
                    caus_m = f[:-1] + er_ends
                    caus_musc_Sg.append(caus_m)
        for caus_end in musc_Sg_end:
            if not pattern_er.endswith('er'):
                caus_m = f + caus_end
                caus_musc_Sg.append(caus_m)

        musc_Sg.append([caus_musc_Sg, musc_trans])

    musc_Pl = []
    musc_Pl_end = ["i", "orum", "is", "os", "is"]  # [Nom, Gen, Dat, Acc, Abl]
    for f_arr in some_arr:
        caus_musc_Pl = []
        forms = f_arr[0]
        translation = f_arr[1]
        musc_trans = (translation[:-2] + 'ые')
        f = (forms[1][:-1])
        pattern_er = (forms[0])
        for caus_end in musc_Pl_end:
            if pattern_er.endswith('er'):
                if pattern_er in exc:
                    caus_m = (f + caus_end)
                else:
                    string = pattern_er[::-1]
                    f = (string.replace('re', 'r', 1))[::-1]
                    caus_m = (f + caus_end)
            else:
                caus_m = (f + caus_end)
            caus_musc_Pl.append(caus_m)
        musc_Pl.append([caus_musc_Pl, musc_trans])
    return musc_Sg, musc_Pl

res12, res13 = making_forms_2_m(res9)
print("Парадигма склонения прил. м.р. ед.ч.:", res12, "\n\n\n", "Парадигма склонения прил. м.р. м.ч.:", res13, "\n\n")

def making_forms_2_n(some_arr):
    neut_Sg = []
    neut_Sg_end = ["um", "i", "o", "um", "o"]
    exc = ["liber", "miser", "asper", "tener"]
    for f_arr in some_arr:
        caus_neut_Sg = []
        forms = f_arr[0]
        translation = f_arr[1]
        neut_trans = (translation[:-2] + 'ое')
        f = (forms[1][:-1])
        pattern_er = (forms[0])
        for caus_end in neut_Sg_end:
            if pattern_er.endswith('er'):
                if pattern_er in exc:
                    caus_n = (f + caus_end)
                else:
                    string = pattern_er[::-1]
                    f = (string.replace('re', 'r', 1))[::-1]
                    caus_n = (f + caus_end)
            else:
                caus_n = (f + caus_end)
            caus_neut_Sg.append(caus_n)
        neut_Sg.append([caus_neut_Sg, neut_trans])

    neut_Pl = []
    neut_Pl_end = ["a", "orum", "is", "a", "is"]  # [Nom, Gen, Dat, Acc, Abl]
    for f_arr in some_arr:
        caus_neut_Pl = []
        forms = f_arr[0]
        translation = f_arr[1]
        neut_trans = (translation[:-2] + 'ые')
        f = (forms[1][:-1])
        pattern_er = (forms[0])
        for caus_end in neut_Pl_end:
            if pattern_er.endswith('er'):
                if pattern_er in exc:
                    caus_n = (f + caus_end)
                else:
                    string = pattern_er[::-1]
                    f = (string.replace('re', 'r', 1))[::-1]
                    caus_n = (f + caus_end)
            else:
                caus_n = (f + caus_end)
            caus_neut_Pl.append(caus_n)
        neut_Pl.append([caus_neut_Pl, neut_trans])
    return neut_Sg, neut_Pl

res14, res15 = making_forms_2_n(res9)
#print("Парадигма склонения прил. ср.р. ед.ч.:", res14, "\n\n", "Парадигма склонения прил. ср.р. мн.ч.:", res15, "\n\n")



def making_forms_3_1(some_arr, gen_arr):   #делает фомрмы прил. 3скл. одного оконч.
    exc = [[['dives', 'divitis'], 'богатый'], [['pauper', 'pauperis'], 'бедный'], [['princeps', 'principis'], 'главный'], [['particeps,', 'participis'], 'ручной']]
    for_exc_Sg = ["i", "em", "e"]  # Dat, Acc, Abl
    trans_ex =[]
    ex_only = []
    for arr_ex in exc:
        check_w = (arr_ex[0][0])
        ex_only.append(check_w)
        tran_ex = (arr_ex[1])
        trans_ex.append(tran_ex)
    m_f_Sg_end = ["i", "em", "i"] #Dat, Acc, Abl
    steams_arr = []
    bas_forms = []
    Gens_only = []
    for gen_f in gen_arr:
        steam = (gen_f[0][:-2])
        steams_arr.append(steam)
        lat_g = (gen_f[0])
        Gens_only.append(lat_g)
    mascul_trans = []
    fem_trans = []
    neut_trans = []
    Pl_trans = []
    f_m_caus = []
    for f_arr in some_arr:
        forms = f_arr[0]
        m_forms = (forms[0])
        bas_forms.append(m_forms)
        translation = (f_arr[1])
        mascul_trans.append(translation)
        femin_trans = (translation[:-2] + 'ая')
        fem_trans.append(femin_trans)
        n_trans = (translation[:-2] + 'ое')
        neut_trans.append(n_trans)
        Pl_tran = (translation[:-2] + 'ые')
        Pl_trans.append(Pl_tran)
        for st in steams_arr:
            if m_forms not in ex_only:
                for caus in m_f_Sg_end:
                    caus_m_f = (st + caus)
                    f_m_caus.append(caus_m_f)
            else:
                for causes in for_exc_Sg:
                    caus_m_f = (st + causes)
                    f_m_caus.append(caus_m_f)
    f_m_caus_2 = [f_m_caus[x:x+3] for x in range(0, len(f_m_caus), 3)]
    Dats = []
    Accs = []
    Abls = []
    for arr in f_m_caus_2:
        Datf = (arr[0])
        Accf = (arr[1])
        Ablf = (arr[2])
        Dats.append(Datf)
        Accs.append(Accf)
        Abls.append(Ablf)
    for i in range(len(gen_arr)):
        gen = (gen_arr[i - 1][0])
        caus_m_f_Sg = [[[x, y, z, q, f], tm, tf] for x, y, z, q, f, tm, tf in
                       zip(bas_forms, Gens_only, Dats, Accs, Abls, mascul_trans, fem_trans)]
        caus_neut_Sg = [[[x, y, z, q, f], tn] for x, y, z, q, f, tn in
                        zip(bas_forms, Gens_only, Dats, bas_forms, Abls, neut_trans)]

    for_exc_Pl_f_m = ["es", "ium", "ibus", "es", "ibus"]  # Gen, Dat, Acc, Abl
    m_f_Pl_end = ["es", "ium", "ibus", "is", "ibus"]  #Non, Gen, Dat, Acc, Abl
    f_m_caus_pl = []
    for st in steams_arr:
        if m_forms not in ex_only:
            for caus in m_f_Pl_end:
                causes_m_f = (st + caus)
                f_m_caus_pl.append(causes_m_f)
        else:
            for causes in for_exc_Pl_f_m:
                causes_m_f = (st + causes)
                f_m_caus_pl.append(causes_m_f)
    f_m_causes_2 = [f_m_caus_pl[x:x + 5] for x in range(0, len(f_m_caus_pl), 5)]
    Noms = []
    Genvs = []
    Dats = []
    Accs = []
    Abls = []
    N_Pl_Nom_Acc = []
    Pl_NOM = []
    for arr in f_m_causes_2:
        Nom = (arr[0][0])
        Pl_NOM.append(Nom)
        N_Nom_Acc = (arr[0][:-2] + 'ia')
        N_Pl_Nom_Acc.append(N_Nom_Acc)
        Nonf = (arr[0])
        Genf = (arr[1])
        Datf = (arr[2])
        Accf = (arr[3])
        Ablf = (arr[4])
        Noms.append(Nonf)
        Genvs.append(Genf)
        Dats.append(Datf)
        Accs.append(Accf)
        Abls.append(Ablf)


    caus_m_f_Pl = [[[x, y, z, q, f], plt] for x, y, z, q, f, plt in zip(Noms, Genvs, Dats, Accs, Abls, Pl_trans)]
    caus_neut_Pl = [[[x, y, z, q, f], tn] for x, y, z, q, f, tn in zip(N_Pl_Nom_Acc, Genvs, Dats, N_Pl_Nom_Acc, Abls, Pl_trans)]

    return caus_m_f_Sg, caus_neut_Sg, caus_m_f_Pl, caus_neut_Pl

res16, res21, res22, res23 = making_forms_3_1(res18, res19)
#print("Прадигма скл. прил 3скл 1 оконч. ж. и м. р. в ед.ч.:",res16,"\n\n","Прадигма скл. прил 3скл 1 оконч. с. р. ед.ч.:", res21,"\n\n", "мн.ч. м. и ж. р.:", res22,"\n\n", "мн.ч. ср. р.:", res23)

def making_3_dec_2_ends(some_arr):
    f_m_caus_Sg_ends = ["is", "i", "em", "i"]    #Gen, Dat, Acc, Abl
    steams = []
    TransM = []
    TransF = []
    MF_forms = []
    TransN = []
    N_forms = []
    Pl_Trans = []
    for f_arr in some_arr:
        f_m_caus_Sg = []
        forms = f_arr[0]
        mf_forms = (forms[0])
        MF_forms.append(mf_forms)
        n_forms = (forms[2])
        N_forms.append(n_forms)
        trans = f_arr[1]
        TransM.append(trans)
        trans_f = trans[:-2] + 'ая'
        TransF.append(trans_f)
        trans_n = trans[:-2] + 'ое'
        TransN.append(trans_n)
        pl_tran = trans[:-2] + 'ие'
        Pl_Trans.append(pl_tran)
        if mf_forms.endswith('es') or mf_forms.endswith('is'):
            steam = (mf_forms[:-2])
        else:
            steam = (mf_forms[:-1])
        steams.append(steam)
        for st in steams:
            for caus in f_m_caus_Sg_ends:
                causes_m_f = (st + caus)
                f_m_caus_Sg.append(causes_m_f)
    for i in TransM:
        f_m_causes_2 = [[f_m_caus_Sg[x:x + 4], i] for x in range(0, len(f_m_caus_Sg), 4)]
    GENs = []
    DATs = []
    ACCs = []
    ABLs = []
    for sup_arr in f_m_causes_2:
        Gen = (sup_arr[0][0])
        GENs.append(Gen)
        Dat = (sup_arr[0][1])
        DATs.append(Dat)
        Acc = (sup_arr[0][2])
        ACCs.append(Acc)
        Abl = (sup_arr[0][3])
        ABLs.append(Abl)

        f_m_Sg_forms = [[[x, y, z, q, f], Tm, Tf] for x, y, z, q, f, Tm, Tf in
                        zip(MF_forms, GENs, DATs, ACCs, ABLs, TransM, TransF)]
        neut_Sg_forms = [[[x, y, z, q, f], Tn] for x, y, z, q, f, Tn in
                         zip(N_forms, GENs, DATs, N_forms, ABLs, TransN)]

    f_m_caus_Pl_ends = ["es", "ium", "ibus", "is", "ibus"]  # Nom, Gen, Dat, Acc, Abl

    f_m_caus_Pl = []
    for st in steams:
        for caus in f_m_caus_Pl_ends:
            causes_m_f = (st + caus)
            f_m_caus_Pl.append(causes_m_f)

    for i in Pl_Trans:
        f_m_causes_3 = [[f_m_caus_Pl[x:x + 5], i] for x in range(0, len(f_m_caus_Pl), 5)]

    Pl_NOM = []
    N_Pl_Nom_Acc = []
    Pl_GEN = []
    Pl_DAT = []
    Pl_ACC = []
    Pl_ABL = []
    for arr in f_m_causes_3:
        Nom = (arr[0][0])
        Pl_NOM.append(Nom)
        N_Nom_Acc = (arr[0][0][:-2] + 'ia')
        N_Pl_Nom_Acc.append(N_Nom_Acc)
        Gen = (arr[0][1])
        Pl_GEN.append(Gen)
        Dat = (arr[0][2])
        Pl_DAT.append(Dat)
        Acc = (arr[0][3])
        Pl_ACC.append(Acc)
        Abl = (arr[0][4])
        Pl_ABL.append(Abl)

        f_m_Pl_forms = [[[x, y, z, q, f], PLT] for x, y, z, q, f, PLT in
                            zip(Pl_NOM, Pl_GEN, Pl_DAT, Pl_ACC, Pl_ABL, Pl_Trans)]
        neut_Pl_forms = [[[x, y, z, q, f], Tn] for x, y, z, q, f, Tn in
                             zip(N_Pl_Nom_Acc, GENs, DATs, N_Pl_Nom_Acc, ABLs, Pl_Trans)]
    return f_m_Sg_forms, neut_Sg_forms, f_m_Pl_forms, neut_Pl_forms

res25, res26, res27, res28 = making_3_dec_2_ends(res20)
# print('Прил 2 окончаний. Парадигма для ж.и м. родов в ед.ч.:',res25,
# '\n\nПрил 2 окончаний. Парадигма для ср. рода в ед.ч.:', res26,
# '\n\nПрил 2 окончаний. Парадигма для ж и м рода во мн.ч.:', res27,
# '\n\nПрил 2 окончаний. Парадигма для ср. рода во мн.ч.:',res28)


def making_3_dec_3_ends(some_arr):
    m_f_ends_Sg = ['is', 'i', 'em', 'i'] #Gen Dat Acc Abl
    M_trans =[]
    F_trans = []
    N_trans = []
    steams = []
    f_m_caus_Sg = []
    m_Noms = []
    f_Noms = []
    n_Noms = []
    Pl_Trans = []
    for f_arr in some_arr:
        forms = f_arr[0]
        m_tran = (f_arr[1])
        M_trans.append(m_tran)
        f_tran = (f_arr[1][:-2] + 'ая')
        F_trans.append(f_tran)
        n_tran = (f_arr[1][:-2] + 'ое')
        N_trans.append(n_tran)
        steam = (f_arr[0][1][:-2])
        steams.append(steam)
        pl_tran = m_tran[:-2] + 'ые'
        Pl_Trans.append(pl_tran)
        m_nom = (forms[0])
        m_Noms.append(m_nom)
        f_nom = (forms[1])
        f_Noms.append(f_nom)
        n_nom = (forms[2])
        n_Noms.append(n_nom)
    for st in steams:
        for caus in m_f_ends_Sg:
            causes_m_f = (st + caus)
            f_m_caus_Sg.append(causes_m_f)
    for i in M_trans:
        f_m_causes_1 = [[f_m_caus_Sg[x:x + 4], i] for x in range(0, len(f_m_caus_Sg), 4)]
    GENs = []
    DATs = []
    ACCs = []
    ABLs = []
    for sup_arr in f_m_causes_1:
        Gen = (sup_arr[0][0])
        GENs.append(Gen)
        Dat = (sup_arr[0][1])
        DATs.append(Dat)
        Acc = (sup_arr[0][2])
        ACCs.append(Acc)
        Abl = (sup_arr[0][3])
        ABLs.append(Abl)

        m_Sg_forms = [[[x, y, z, q, f], Tm] for x, y, z, q, f, Tm in
                        zip(m_Noms, GENs, DATs, ACCs, ABLs, M_trans)]
        f_Sg_forms = [[[x, y, z, q, f], Tf] for x, y, z, q, f, Tf in
                        zip(f_Noms, GENs, DATs, ACCs, ABLs, F_trans)]
        neut_Sg_forms = [[[x, y, z, q, f], Tn] for x, y, z, q, f, Tn in
                         zip(n_Noms, GENs, DATs, n_Noms, ABLs, N_trans)]

    m_f_ends_Pl = ['es', 'ium', 'ibus', 'is', 'ibus']  # Nom Gen Dat Acc Abl

    f_m_caus_Pl = []
    for st in steams:
        for caus in m_f_ends_Pl:
            causes_m_f = (st + caus)
            f_m_caus_Pl.append(causes_m_f)

    for i in Pl_Trans:
        f_m_causes_2 = [[f_m_caus_Pl[x:x + 5], i] for x in range(0, len(f_m_caus_Pl), 5)]

    Pl_NOM = []
    N_Pl_Nom_Acc = []
    Pl_GEN = []
    Pl_DAT = []
    Pl_ACC = []
    Pl_ABL = []
    for arr in f_m_causes_2:
        Nom = (arr[0][0])
        Pl_NOM.append(Nom)
        N_Nom_Acc = (arr[0][0][:-2] + 'ia')
        N_Pl_Nom_Acc.append(N_Nom_Acc)
        Gen = (arr[0][1])
        Pl_GEN.append(Gen)
        Dat = (arr[0][2])
        Pl_DAT.append(Dat)
        Acc = (arr[0][3])
        Pl_ACC.append(Acc)
        Abl = (arr[0][4])
        Pl_ABL.append(Abl)

        f_m_Pl_forms = [[[x, y, z, q, f], PLT] for x, y, z, q, f, PLT in
                        zip(Pl_NOM, Pl_GEN, Pl_DAT, Pl_ACC, Pl_ABL, Pl_Trans)]
        neut_Pl_forms = [[[x, y, z, q, f], Tn] for x, y, z, q, f, Tn in
                         zip(N_Pl_Nom_Acc, Pl_GEN, Pl_DAT, N_Pl_Nom_Acc, Pl_ABL, Pl_Trans)]

    return m_Sg_forms, f_Sg_forms, neut_Sg_forms, f_m_Pl_forms, neut_Pl_forms

res29, res30, res31, res32, res33 = making_3_dec_3_ends(res24)
# print(res29,'\n',  res30, '\n', res31, '\n', res32, '\n', res33)
# print('Прил. 3скл. 3 оконч. ж.р. ед.ч.:',res30, '\n\n',
#       'Прил. 3скл. 3 оконч. ср.р. ед.ч.:',res31, '\n\n',
#       'Прил. 3скл. 3 оконч. м.и ж. р. мн.ч.:',res32, '\n\n',
#       'Прил. 3скл. 3 оконч. ср.р. мн.ч.:', res33)

def craft_diction_forms(dec1_Sg, dec1_Pl, dec2_m_Sg, dec2_m_Pl, dec2_n_Sg, dec2_n_Pl, dec3_1end_mf_Sg, dec3_1end_n_Sg,
                        dec3_1end_mf_Pl, dec3_1end_n_Pl, dec3_2ends_mf_Sg, dec3_2ends_n_Sg, dec3_2ends_mf_Pl,
                        dec3_2ends_n_Pl, dec3_3ends_m_Sg, dec3_3ends_f_Sg, dec3_3ends_n_Sg, dec3_3ends_mf_Pl, dec3_3ends_n_Pl, user_word):


    for idx in range(len(dec1_Sg)):     # dec1_2

        cases = ["Nom", "Gen", "Dat", "Acc", "Abl"]

        nom_m = dec2_m_Sg[idx][0]
        if user_word in nom_m:
            num_word = idx
            print(dec2_m_Sg[idx][1])
            print("падеж\tm\tf\tn")

            for case_idx, case in enumerate(cases):
                search_f_sg = dec1_Sg[num_word]
                search_m_sg = dec2_m_Sg[num_word]
                search_n_sg = dec2_n_Sg[num_word]
                print('\t'.join([case,
                                 search_f_sg[0][case_idx],
                                 search_m_sg[0][case_idx],
                                 search_n_sg[0][case_idx]]))
            print()
            print()
            print()

            print(dec2_m_Pl[idx][1])
            print("падеж\tm\tf\tn")
            for case_idx, case in enumerate(cases):
                search_f_pl = dec1_Pl[num_word]
                search_m_pl = dec2_m_Pl[num_word]
                search_n_pl = dec2_n_Pl[num_word]
                print('\t'.join([case,
                                 search_f_pl[0][case_idx],
                                 search_m_pl[0][case_idx],
                                 search_n_pl[0][case_idx]]))

            print()
            print()
            print()


    for idx in range(len(dec3_1end_mf_Sg)):     # dec3_1end

        cases = ["Nom", "Gen", "Dat", "Acc", "Abl"]

        nom_m = dec3_1end_mf_Sg[idx][0]
        if user_word in nom_m:
            num_word = idx
            print(dec3_1end_mf_Sg[idx][1])
            print("падеж\tm\tf\tn")

            for case_idx, case in enumerate(cases):
                search_fm_sg = dec3_1end_mf_Sg[num_word]
                search_n_sg = dec3_1end_n_Sg[num_word]
                print('\t'.join([case,
                                 search_fm_sg[0][case_idx],
                                 search_fm_sg[0][case_idx],
                                 search_n_sg[0][case_idx]]))
            print()
            print()
            print()

            print(dec3_1end_mf_Pl[idx][1])
            print("падеж\tm\tf\tn")
            for case_idx, case in enumerate(cases):
                search_fm_pl = dec3_1end_mf_Pl[num_word]
                search_n_pl = dec3_1end_n_Pl[num_word]
                print('\t'.join([case,
                                 search_fm_pl[0][case_idx],
                                 search_fm_pl[0][case_idx],
                                 search_n_pl[0][case_idx]]))

            print()
            print()
            print()

    for idx in range(len(dec3_2ends_mf_Sg)):  # dec3_2ends

        cases = ["Nom", "Gen", "Dat", "Acc", "Abl"]

        nom_m = dec3_2ends_mf_Sg[idx][0]
        if user_word in nom_m:
            num_word = idx
            print(dec3_2ends_mf_Sg[idx][1])
            print("падеж\tm\tf\tn")

            for case_idx, case in enumerate(cases):
                search_fm_sg = dec3_2ends_mf_Sg[num_word]
                search_n_sg = dec3_2ends_n_Sg[num_word]
                print('\t'.join([case,
                                 search_fm_sg[0][case_idx],
                                 search_fm_sg[0][case_idx],
                                 search_n_sg[0][case_idx]]))
            print()
            print()
            print()

            print(dec3_2ends_mf_Pl[idx][1])
            print("падеж\tm\tf\tn")
            for case_idx, case in enumerate(cases):
                search_fm_pl = dec3_2ends_mf_Pl[num_word]
                search_n_pl = dec3_2ends_n_Pl[num_word]
                print('\t'.join([case,
                                 search_fm_pl[0][case_idx],
                                 search_fm_pl[0][case_idx],
                                 search_n_pl[0][case_idx]]))

            print()
            print()
            print()

    for idx in range(len(dec3_3ends_m_Sg)):  # dec3_3ends

        cases = ["Nom", "Gen", "Dat", "Acc", "Abl"]

        nom_m = dec3_3ends_m_Sg[idx][0]
        if user_word in nom_m:
            num_word = idx
            print(dec3_3ends_m_Sg[idx][1])
            print("падеж\tm\tf\tn")

            for case_idx, case in enumerate(cases):
                search_f_sg = dec3_3ends_f_Sg[num_word]
                search_m_sg = dec3_3ends_m_Sg[num_word]
                search_n_sg = dec3_3ends_n_Sg[num_word]
                print('\t'.join([case,
                                 search_f_sg[0][case_idx],
                                 search_m_sg[0][case_idx],
                                 search_n_sg[0][case_idx]]))
            print()
            print()
            print()

            print(dec2_m_Pl[idx][1])
            print("падеж\tm\tf\tn")
            for case_idx, case in enumerate(cases):
                search_fm_pl = dec3_3ends_mf_Pl[num_word]
                search_n_pl = dec3_3ends_n_Pl[num_word]
                print('\t'.join([case,
                                 search_fm_pl[0][case_idx],
                                 search_fm_pl[0][case_idx],
                                 search_n_pl[0][case_idx]]))

            print()
            print()
            print()
    return 1

res34 = craft_diction_forms(res10, res11, res12, res13, res14, res15, res16, res21, res22, res23, res25, res26, res27,
                           res28, res29, res30, res31, res32, res33, res200)
# print(res34)