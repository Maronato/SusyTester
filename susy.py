import subprocess
import requests
from os.path import dirname, abspath, exists
from os import makedirs
import warnings
import sys

# ALTERE A SUA TURMA AQUI:
turma = "mc102mn"
# EXEMPLO: "mc102mn"
# COM AS ÁSPAS!
# ÓTIMO. NÃO PRECISA ALTERAR MAIS NADA.

url = 'https://susy.ic.unicamp.br:9999/' + turma + "/"

base_dir = dirname(dirname(abspath(__file__)))


class Problem:
    """Problema

    Classe que roda os problemas e pá

    Args:
        number (int): Número do lab. Ex: 5, pro lab05
        pset (int, opcional): Testinho que vai ser executado
    """

    def __init__(self, number, pset=1):
        def base10(n):
            if n < 10:
                return "0" + str(n)
            return str(n)

        self.pset = base10(pset)
        self.number = base10(number)
        self.inp_url = "{}{}/dados/arq{}.in".format(url, self.number, self.pset)
        self.res_url = "{}{}/dados/arq{}.res".format(url, self.number, self.pset)
        self.program = "{}/lab{}/lab{}".format(base_dir, self.number, self.number)

    def validate(self):
        """Validate

        Checa se o testinho existe. Se existir, baixa a entrada e saída

        Returns:
            True se testinho existe, False caso contrário
        """
        with warnings.catch_warnings():
            # Susy está com o certificado vencido, então ignora os alertas do requests
            warnings.simplefilter("ignore")
            self.cache_download()
        if self.stdin.find("Página inexistente ou inacessível") != -1:
            return False
        return True

    def cache_download(self):
        """Cache / Download

        Baixa ou carrega do disco as entradas e saídas do testinho
        """
        # Processa o stdin salvo no disco
        if exists("{}/lab{}/in/pset{}.txt".format(base_dir, self.number, self.pset)):
            with open("{}/lab{}/in/pset{}.txt".format(base_dir, self.number, self.pset), 'r') as f:
                self.stdin = f.read()
        # Baixa o stdin, processa e salva no disco
        else:
            makedirs(dirname("{}/lab{}/in/pset{}.txt".format(base_dir, self.number, self.pset)), exist_ok=True)
            self.stdin = requests.get(self.inp_url, verify=False).text
            with open("{}/lab{}/in/pset{}.txt".format(base_dir, self.number, self.pset), 'w+') as f:
                f.write(self.stdin)
        # A mesma coisa, só que pro res
        if exists("{}/lab{}/out/pset{}.txt".format(base_dir, self.number, self.pset)):
            with open("{}/lab{}/out/pset{}.txt".format(base_dir, self.number, self.pset), 'r') as f:
                self.res_list = f.read().split('\n')
        else:
            makedirs(dirname("{}/lab{}/out/pset{}.txt".format(base_dir, self.number, self.pset)), exist_ok=True)
            res_string = requests.get(self.res_url, verify=False).text
            with open("{}/lab{}/out/pset{}.txt".format(base_dir, self.number, self.pset), 'w+') as f:
                f.write(res_string)
            self.res_list = res_string.split('\n')

    def run(self, args=""):
        """Run

        Roda o programa usando a entrada ali de cima e salva as respostas

        Args:
            args (str, opcional): Argumentos que devem ser passados pro programa
        Returns:
            True se o testinho rodou sem erros de execução, False caso contrário
        """
        path = "{} {}".format(self.program, args) if args else "{}".format(self.program)
        process = subprocess.Popen(path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        inp, out, err = process.stdin, process.stdout, process.stderr
        for line in self.stdin.split('\n'):
            try:
                inp.write((line + '\n').encode('utf-8'))
            except BrokenPipeError:
                break
        try:
            inp.close()
        except BrokenPipeError:
            pass
        self.stdout = out.read().decode('latin1')
        self.stderr = err.read().decode('latin1')
        out.close()
        err.close()
        process.wait()
        if self.stderr:
            print(self.stderr)
            return False
        return True

    def stdout_to_list(self):
        """Converte o stdout pra uma lista"""
        return self.stdout.split('\n')

    def compare(self):
        """Compare

        Compara os seus resultados com os esperados
        pelo susy

        Returns:
            True se deu bom, False caso contrário
        """
        my_results = self.stdout_to_list()
        res_results = self.res_list
        success = True
        for i, val in enumerate(my_results):

            try:
                current = res_results[i]
            except IndexError:
                current = ''

            if val != current:
                print()
                print("Erro na saida {} do teste {}".format(i, self.pset))
                print('Sua saida foi:\n"{}"\ne deveria ter sido:\n"{}"\n'.format(val, current))
                success = False

        return success


def test_labs(number, i, j):
    """Test Labs

    Roda os testinhos de i até j

    Args:
        number (int): Número do lab
        i (int, opcional): Número do primeiro testinho a ser testado
        j (int, opcional): Número do último testinho a ser testado
    """
    i = i or 1
    j = j or 50
    errors = 0
    for i in range(i, j):
        lab = Problem(number, i)
        if lab.validate():
            run = lab.run()
            if not run:
                print("Erro rodando o lab {}, teste {}".format(number, i))
                print(run)
                print()
            else:
                comp = lab.compare()
                if comp:
                    print("Teste {} OK".format(i))
                else:
                    errors += 1
        else:
            er = "sem erros" if not errors else (("com " + str(errors) + " erros") if errors > 1 else ("com " + str(errors) + " erro"))
            msg = "Terminando testes " + er
            print(msg)
            break


if __name__ == "__main__":
    """Main

    Normalmente você vai rodar isso aqui

    Args:
        1 (int): número do lab
        2 (int, opcional): Testinho inicial
        3 (int, opcional): Testinho final
    """
    if len(sys.argv) not in [2, 3, 4]:
        print("Número errado de argumentos")
    else:
        test_labs(int(sys.argv[1]), int(sys.argv[2]) if 2 < len(sys.argv) else None, int(sys.argv[3]) if 3 < len(sys.argv) else None)
