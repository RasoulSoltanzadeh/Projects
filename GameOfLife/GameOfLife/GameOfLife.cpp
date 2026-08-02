///In The Name Of God
///Date: 2024/06/01 - 1404/10/8
///Author: Rasoul Soltanzadeh - AmirHossein Abyazinezhad
///Proffesor: Dr. Babagoli
///TA-Programming: Mr. Mahdi Zabihi
///Environment: Visual Studio 2022 - Console Application
///Language: C++23
///Project Name: Game of Life
///University: University of Mazandaran - Iran
///Field of study: Computer Engineering
///Course Name: Computer Science
///Description:  
/// Game of Life  
/// Project 3: Bazi Zendegi
/// Bazi ye cell - based simulation e ke dar 1971 tavasot John Conway ejaad shod.
/// Ye mesal az bazi bedune bazikon hast.Har cell dar har nasl mitune zende ya mordeh bashe,
/// va ghanon haye bazi moshakhas mikonan ke che etefaqi miofte.Bazi be soorat bi taraf va bi payan tashkil mishe.
/// Har nasl, cell ha ya zende mimunan ya mimiran.
/// Ghavanin Conway :
/// Agar ye cell zende kamtar az do hamsaye zende dashte bashe, mimire.
/// Agar ye cell zende bishtar az se hamsaye zende dashte bashe, mimire.
/// Agar ye cell zende do ya se hamsaye zende dashte bashe, zende mimune.
/// Agar ye cell mordeh daghighan se hamsaye zende dashte bashe, zende mishe.
/// Tazakorat ejra :
/// Dar in project, tarahi shoma bayad bi payan va mahdood nabashe.
/// Cell haye kenari ro mitunin farz konin mordeh hastan.
/// Baraye namayesh mitunin az ‘* ’ baraye cell zende va ‘.’ baraye cell mordeh estefade konin.
/// Barname bayad dar har nasl vaziyat ro namayesh bede va nasl badi ro hesab kone.
/// Bazi tori tarahi shode ke karbar chinesh avaliye cell ha ro taeen mikone va bazi baghie nasl ha ro khodesh misaze.
#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

//In method barresi mikonad ke mokhtasat daryaft shode dar mahdude safhe hast ya na.
bool IsInBound(int size, int i, int j)
{
    return ((i > -1) && (i < size) && (j > -1) && (j < size));
}

//In method cell haye dor o bardar cell morede nazar ra bar migardanad.
vector<bool> GetAroundCells(vector<vector<bool>> board, int i, int j)
{
    vector<bool> result;
    int indexes[8][2] = { {i - 1, j - 1}, {i, j - 1}, {i + 1, j - 1}, {i - 1, j}, {i + 1, j}, {i - 1, j + 1}, {i, j + 1}, {i + 1, j + 1} };
    int size = board.size();
    for (int i = 0; i < 8; i++)
        if (IsInBound(size, indexes[i][0], indexes[i][1])) result.push_back(board[indexes[i][0]][indexes[i][1]]);
    return result;
}

//In method tedad cell haye zende ra bar migardanad.
int GetAliveCellsCount(vector<bool> cells)
{
    int count = 0;
    for (bool cell : cells)
        if (cell) count++;
    return count;
}

//In method vaziate cell morede nazar dar nasl badi ra bar migardanad.
bool SetCellState(vector<vector<bool>> board, int i, int j)
{
    int aliveCellsCount = GetAliveCellsCount(GetAroundCells(board, i, j));
    if (board[i][j]) return (aliveCellsCount == 2 || aliveCellsCount == 3);
    else return (aliveCellsCount == 3);
}

//In method nasl badi board ra bar migardanad.
vector<vector<bool>> GetNextGeneration(vector<vector<bool>> board, int size)
{
    vector<vector<bool>> result;
    for (int i = 0; i < size; i++)
    {
        vector<bool> resultRow;
        for (int j = 0; j < size; j++) resultRow.push_back(SetCellState(board, i, j));
        result.push_back(resultRow);
    }
    return result;
}

//In method board ra az halat boolean be halat string tabdil mikonad.
vector<string> ConvertToStringBoard(vector<vector<bool>> board)
{
    vector<string> result;
    for (auto boolLine : board)
    {
        string stringLine;
        for (bool cell : boolLine)
        {
            if (cell) stringLine += "* ";
            else stringLine += ". ";
        }
        result.push_back(stringLine);
    }
    return result;
}

//In method board ra az halat string be halat boolean tabdil mikonad.
vector<vector<bool>> ConvertToBooleanBoard(vector<string> stringBoard)
{
    vector<vector<bool>> result;
    for (string stringLine : stringBoard)
    {
        vector<bool> boolLine;
        for (char ch : stringLine)
        {
            if (ch == '*') boolLine.push_back(true);
            else boolLine.push_back(false);
        }
        result.push_back(boolLine);
    }
    return result;
}

//In method barresi mikonad ke khat vared shode sahih ast ya na.
bool IsStringInputLineIncorrect(string line, int size)
{
    return ((line.length() == size) && all_of(line.begin(), line.end(), [](char c) { return c == '.' || c == '*'; }));
}

//In method board ra az karbar migirad.
vector<string> GetStringBoardInput(int size)
{
    vector<string> result;
    string inputLine;
    cout << "\nAttending to the size, Please enter the board, using '.' for dead cells and '*' for alive cells without any another characters:" << endl;
    for (int i = 0; i < size; i++)
    {
        cin >> inputLine;
        if (IsStringInputLineIncorrect(inputLine, size)) result.push_back(inputLine);
        else
        {
            cout << "\nIncorrect input line. Please enter again.\n" << endl;
            i--;
        }
    }
    return result;
}

//In method az karbar mikhahad taeen konad ke aya mikhahad nasl badi namayesh dade shavad ya na.
bool CanGenerateNextGeneration(string message)
{
    string answer;
    cout << message;
    cout << "\nDo you want to see the next generation? (Yes/No): ";
    cin >> answer;
    return answer == "Yes" ? true : answer == "No" ? false : CanGenerateNextGeneration("\n  The answer is not valid. Try again.\n");
}

//In method board ra namayesh midahad.
void ShowBoard(vector<string> board)
{
    for (string line : board) cout << line << endl;
}

//Barnameye asli
int main()
{
    int size = 0;
    cout << "Please enter the size of the board (size x size): ";
    cin >> size;

    vector<string> stringBoard = GetStringBoardInput(size);
    vector<vector<bool>> booleanBoard = ConvertToBooleanBoard(stringBoard);

    cout << "\nYour board is:" << endl;
    ShowBoard(stringBoard);

    while (true)
    {
        if (!CanGenerateNextGeneration("")) break;
        cout << "\nNext generation board is:" << endl;
        vector<vector<bool>> nextGenerationBoard = GetNextGeneration(booleanBoard, size);
        ShowBoard(ConvertToStringBoard(nextGenerationBoard));
        booleanBoard = nextGenerationBoard;
    }
    return 0;
}