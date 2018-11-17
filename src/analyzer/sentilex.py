
class Sentilex(object):

    def get_sentilex_dictionary(self):
        sentilexpt = open('sentilex-lem-pt01.txt', 'r')
        dicionario_palavra_polaridade = {}
        for i in sentilexpt.readlines():
            pos_ponto = i.find('.')
            palavra = (i[:pos_ponto])
            pol_pos = i.find('POL')
            polaridade = (i[pol_pos + 4:pol_pos + 6]).replace(';', '')
            dicionario_palavra_polaridade[palavra] = polaridade
        return dicionario_palavra_polaridade

    def get_score_phrase(frase, dicionario_palavra_polaridade):
        l_sentimento = []
        for p in frase.split():
            l_sentimento.append(int(dicionario_palavra_polaridade.get(p, 0)))
        score = sum(l_sentimento)
        if score > 0:
            return 'Positivo'
        elif score == 0:
            return 'Neutro'
        else:
            return 'Negativo'
