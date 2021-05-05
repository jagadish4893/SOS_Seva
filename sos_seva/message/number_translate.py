lang_number={'hi':['०','१','२','३','४','५','६','७','८','९'],
             'gu':['૦','૧','૨','૩','૪','૫','૬','૭','૮','૯'],
             'en':['0','1','2','3','4','5','6','7','8','9'],
             'mr':['०','१','२','३','४','५','६','७','८','९'],
             'bn':['০','১','২','৩','৪','৫','৬','৭','৮','৯'],
             'te':['౦','౧','౨','౩','౪','౫','౬','౭','౮','౯'],
             'ta':['0','௧','௨','௩','௪','௫','௬','௭','௮','௯'],
             'pa':['੦','੧','੨','੩','੪','੫','੬','੭','੮','੯'],
             'ml':['൦','൧','൨','൩','൪','൫','൬','൭','൮','൯'],
             'or':['୦','୧','୨','୩','୪','୫','୬','୭','୮','୯'],
             'kn':['೦','೧','೨','೩','೪','೫','೬','೭','೮','೯']
             }


def get_pincode(pincode,user_lang):
    list_pincode=list(pincode)
    lang_list=lang_number[user_lang]
    res = [(lang_list).index(i) for i in list_pincode]
    english_pincode = str("".join([str(i) for i in res]))
    print(english_pincode)
    return english_pincode

