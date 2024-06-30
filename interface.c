#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include <time.h>
#include <stdlib.h>

int x, missao = 0;
int origemCanhao0 = 53, origemCanhao1 = 93;
int contaRefem = 10;
int contaResgatado = 0;
int posicaoHelice = 0;
int posicaRoda[2] = {0, 0};
int canhaoMovendo[2] = {0, 0};

// Fun��o gotoxy
void gotoxy(int x, int y)
{
    COORD coord;
    coord.X = x;
    coord.Y = y;
    SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), coord);
}

void explode_bomba(int x, int y)
{
    gotoxy(x, y);
    printf("*");
    Sleep(50);
    printf(" ");
    gotoxy(x, y - 1);
    printf("O");
    gotoxy(x - 1, y);
    printf("O O");
    gotoxy(x, y + 1);
    printf("O");
    Sleep(50);
    gotoxy(x, y - 1);
    printf(" ");
    gotoxy(x - 1, y);
    printf("   ");
    gotoxy(x, y + 1);
    printf(" ");

    gotoxy(x, y - 2);
    printf("o");
    gotoxy(x - 2, y);
    printf("o   o");
    gotoxy(x, y + 2);
    printf("o");
    Sleep(50);
    gotoxy(x, y - 2);
    printf(" ");
    gotoxy(x - 2, y);
    printf("     ");
    gotoxy(x, y + 2);
    printf(" ");
}
void helicopteroE2D(int x, int y)
{
    gotoxy(x + 3, y);
    switch (posicaoHelice)
    {
    case 0:
        printf("______+______\n");
        break;
    case 1:
        printf(" _____+_____ \n");
        break;
    case 2:
        printf("  ____+____  \n");
        break;
    case 3:
        printf("   ___+___   \n");
        break;
    case 4:
        printf("    __+__    \n");
        break;
    case 5:
        printf("     _+_    \n");
        break;
    case 6:
        printf("    __+__    \n");
        break;
    case 7:
        printf("   ___+___   \n");
        break;
    case 8:
        printf("  ____+____  \n");
        break;
    case 9:
        printf(" _____+_____ \n");
        break;
    case 10:
        printf("______+______\n");
        break;
    }
    posicaoHelice = (posicaoHelice < 10 ? posicaoHelice + 1 : 1);
    gotoxy(x + 7, y + 1);
    printf("__|__\n");
    gotoxy(x, y + 2);
    printf("/\\====/     \\\n");
    gotoxy(x, y + 3);
    printf("      \\      )\n");
    gotoxy(x, y + 4);
    printf("       _+@_+_\n");
}
void helicopteroD2E(int x, int y)
{
    gotoxy(x - 2, y);
    switch (posicaoHelice)
    {
    case 0:
        printf("______+______\n");
        break;
    case 1:
        printf(" _____+_____ \n");
        break;
    case 2:
        printf("  ____+____  \n");
        break;
    case 3:
        printf("   ___+___   \n");
        break;
    case 4:
        printf("    __+__    \n");
        break;
    case 5:
        printf("     _+_    \n");
        break;
    case 6:
        printf("    __+__    \n");
        break;
    case 7:
        printf("   ___+___   \n");
        break;
    case 8:
        printf("  ____+____  \n");
        break;
    case 9:
        printf(" _____+_____ \n");
        break;
    case 10:
        printf("______+______\n");
        break;
    }
    posicaoHelice = (posicaoHelice < 10 ? posicaoHelice + 1 : 1);
    gotoxy(x + 2, y + 1);
    printf("__|__\n");
    gotoxy(x + 1, y + 2);
    printf("/     \\====/\\\n");
    gotoxy(x, y + 3);
    printf("(      /\n");
    gotoxy(x + 2, y + 4);
    printf("_+__+_       \n");
}
void apaga_helicopteroE2D(int x, int y)
{
    gotoxy(x, y);
    printf("               \n");
    gotoxy(x, y + 1);
    printf("               \n");
    gotoxy(x, y + 2);
    printf("               \n");
    gotoxy(x, y + 3);
    printf("               \n");
    gotoxy(x, y + 4);
    printf("               \n");
}

void bomba(int x, int y, int posicao)
{
    for (; y > 0; y--)
    {
        gotoxy(x, y);
        printf("o\n");
        Sleep(20);
        gotoxy(x, y);
        printf(" \n");
        switch (posicao)
        {
        case -1:
            x--;
            break;
        case 0:
            x;
            break;
        case 1:
            x++;
        }
    }
}

void inicializaCanhao(int x, int y, int canhao)
{
    int posicao;
    char roda = 'O';
    time_t t;
    if (canhaoMovendo[canhao])
    {
        switch (posicaRoda[canhao])
        {
        case 0:
            roda = '|';
            break;
        case 1:
            roda = '/';
            break;
        case 2:
            roda = '-';
            break;
        case 3:
            roda = '\\';
            break;
        }
        posicaRoda[canhao] = (posicaRoda[canhao] < 3 ? posicaRoda[canhao] + 1 : 0);
    }
    gotoxy(x, y + 1);
    printf(" ___+--+___");
    gotoxy(x, y + 2);
    printf("/          \\");
    gotoxy(x, y + 3);
    printf("\\          /");
    gotoxy(x, y + 4);
    printf(" -%c-%c--%c-%c-", roda, roda, roda, roda);
    gotoxy(x, y);
    printf("     ||");
}
void canhaoAtira(int x, int y)
{
    int posicao;
    time_t t;
    gotoxy(x, y + 1);
    printf(" ___+--+___");
    gotoxy(x, y + 2);
    printf("/          \\");
    gotoxy(x, y + 3);
    printf("\\          /");
    gotoxy(x, y + 4);
    printf(" -O-O--O-O-");
    gotoxy(x, y);
    srand((unsigned)time(&t));
    for (int foguete = 3; foguete > 0; foguete--)
    {
        posicao = (rand() % 3) - 1;
        gotoxy(0, 28);
        printf("%6d  %6d\n", foguete, posicao);
        gotoxy(x, y);
        switch (posicao)
        {
        case -1:
            printf("     \\\\\n");
            break;
        case 0:
            printf("     ||");
            break;
        case 1:
            printf("     //");
        }
        bomba(x + 5, y - 1, posicao);
    }
}

void apagaCanhao(int x, int y)
{
    int posicao;
    time_t t;
    gotoxy(x, y + 1);
    printf("           ");
    gotoxy(x, y + 2);
    printf("            ");
    gotoxy(x, y + 3);
    printf("            ");
    gotoxy(x, y + 4);
    printf("           ");
    gotoxy(x, y);
    printf("       ");
}

void moveCanhaoD2E(int origem, int Destino, int canhao)
{
    for (int x = origem; x > Destino;)
    {
        Sleep(50);
        apagaCanhao(x, 20);
        inicializaCanhao(--x, 20, canhao);
    }
}

void moveCanhaoE2D(int origem, int Destino, int canhao)
{
    for (int x = origem; x <= Destino;)
    {
        Sleep(50);
        apagaCanhao(x, 20);
        inicializaCanhao(++x, 20, canhao);
    }
}

void plataformaE(void)
{
    int linha;
    gotoxy(0, 7);
    printf("----------+\n");
    gotoxy(0, 8);
    printf("|         /\n");
    for (linha = 9; linha < 25; linha++)
    {
        gotoxy(0, linha);
        printf("|        |\n");
    }
}
void desenhaRefens(void)
{
    gotoxy(0, 6);
    printf("          ");
    for (int i = 0; i < contaRefem; i++)
    {
        gotoxy(0 + i, 6);
        printf("@");
    }
}

void desenhaResgatados(void)
{
    for (int i = 0; i < contaResgatado; i++)
    {
        gotoxy(109 + i, 6);
        printf("@");
    }
}
void plataformaD(void)
{
    int linha;
    gotoxy(108, 7);
    printf("+-----------\n");
    gotoxy(109, 8);
    printf("\\         \n");
    for (linha = 9; linha < 25; linha++)
    {
        gotoxy(109, linha);
        printf(" |        | \n");
    }
}

void ponte(void)
{
    gotoxy(30, 25);
    printf("+-----------------------+\n");
    gotoxy(30, 26);
    printf("|         ---           |\n");
    gotoxy(30, 27);
    printf("|        /   \\          |\n");
    gotoxy(30, 28);
    printf("|       /     \\         |\n");
    gotoxy(30, 29);
    printf("|      /       \\        |\n");
}
void deposito(void)
{
    gotoxy(0, 20);
    printf("|\\|\\|\\|\\|\\|\\|\\|\\|\\|\\|\\");
    gotoxy(0, 21);
    printf("|                     |");
    gotoxy(0, 22);
    printf("|       +----+        |");
    gotoxy(0, 23);
    printf("|       |    |        |");
    gotoxy(0, 24);
    printf("|       |    |        |");
}
int main()
{
    int coluna = 5;
    int linha = 3;
    int k = 0;
    system("cls");
    gotoxy(0, 25);
    for (coluna = 0; coluna < 120; coluna++)
    {
        printf("^");
    }
    inicializaCanhao(origemCanhao0, 20, 0);
    inicializaCanhao(origemCanhao1, 20, 1);
    ponte();
    plataformaE();
    desenhaRefens();
    deposito();
    plataformaD();

    canhaoAtira(origemCanhao0, 20);      // Canhao Dispara
    canhaoMovendo[0] = 1;                // Canhao 0 em movimento para recarregar
    moveCanhaoD2E(origemCanhao0, 23, 0); // Canhao 0 vai recarregar
    canhaoMovendo[0] = 0;                // Canhao 0 parado
    Sleep(1000);                         // Carregando canhao 0

    canhaoMovendo[0] = 1; // Canhao 0 em movimento
    moveCanhaoE2D(23, origemCanhao0, 0);
    canhaoMovendo[0] = 0;           // Canhao 0 parado
    canhaoAtira(origemCanhao0, 20); // Canhao 0 Dispara

    canhaoAtira(origemCanhao1, 20);
    canhaoMovendo[1] = 1;                // Canhao 1 em movimento
    moveCanhaoD2E(origemCanhao1, 23, 1); // Canhao 0 vai recarregar
    canhaoAtira(origemCanhao0, 20);      // Canhao 0 Dispara (ele havia sido "apagado" por 1)
    canhaoMovendo[1] = 0;                // Canhao 1 parado
    Sleep(1000);                         // Carregando canhao 1

    canhaoMovendo[1] = 1; // Canhao 1 em movimento
    moveCanhaoE2D(23, origemCanhao1, 1);
    canhaoAtira(origemCanhao0, 20); // Canhao 0 Dispara (ele havia sido "apagado" por 1)
    canhaoMovendo[1] = 0;           // Canhao 1 parado
    canhaoAtira(origemCanhao1, 20); // Canhao 1 Dispara

    for (int i = 0; i < 7; i++)
    { // Bombas explodem no ar
        explode_bomba((rand() % 70) + 10, (rand() % 10) + 4);
        Sleep(1000);
    }

    while (contaRefem)
    {
        contaRefem--; // Mais um refem buscado
        desenhaRefens();
        for (coluna = 0; coluna < 100; coluna++)
        {
            helicopteroE2D(coluna, 0);
            Sleep(100);
            apaga_helicopteroE2D(coluna, 0);
        }
        contaResgatado++; // Mais um refem resgatado
        desenhaResgatados();
        for (coluna = 99; coluna > 7; coluna--)
        {
            helicopteroD2E(coluna, 0);
            Sleep(100);
            apaga_helicopteroE2D(coluna, 0);
        }
    }
    getche();
}