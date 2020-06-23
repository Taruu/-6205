#define SERIAL_BUFFER_SIZE 2024
//TODO var19B
//Переключение
const int var8A = 13;

const int var6A = 11;
const int var6B = 12;

const int var10A = 10;
const int var12A = 9;
const int var15B = 8;
const int var16A = 7;

//take symbol
const int var22A = A0;
const int var22B = A1;
const int var20B = A6;
const int var24A = A2;
const int var23B = A7;
const int var18B = A5;
const int var24B = A3;
const int var16B = A4;

//take screen
const int var2A = 5;
const int var2B = 6;
//clear screen
const int var18A = 4;

byte clearCount = 0;
int nowPosCursor = 0; //Позиция курсора 

int cursorFlash = 0;


void setup() {
  pinMode (var8A, OUTPUT);
  
  pinMode (var6A, OUTPUT);
  pinMode (var6B, OUTPUT);
  
  pinMode (var10A, OUTPUT);
  pinMode (var12A, OUTPUT);
  
  pinMode (var15B, OUTPUT);
  pinMode (var16A, OUTPUT);

  pinMode ( var22A, OUTPUT);
  pinMode ( var22B, OUTPUT);
  pinMode ( var20B, OUTPUT);
  pinMode ( var24A, OUTPUT);
  pinMode ( var23B, OUTPUT);
  pinMode ( var18B, OUTPUT);
  pinMode ( var24B, OUTPUT);
  pinMode ( var16B, OUTPUT);

  pinMode ( var2A, OUTPUT);
  pinMode ( var2B, OUTPUT);
  
  pinMode ( var18A, OUTPUT);

  
  // put your setup code here, to run once:
  setCursor(false);// курсор


  digitalWrite(var10A,LOW);
  digitalWrite(var12A,LOW);

  
  digitalWrite(var6B,HIGH);
  digitalWrite(var6A,HIGH);
  digitalWrite(var15B,HIGH);
  digitalWrite(var16A,HIGH);

  digitalWrite(var18A,HIGH);

  Serial.begin(115200);
  delay(20);
  Serial.println("r");
  
}

void loop() {
  if (Serial.available()>0){
    int needRead = Serial.read();
    commandHandler(needRead);
   }
  
}


void commandHandler(int serialCountByte){
  byte listCommandBytes[serialCountByte];
  Serial.print( serialCountByte);
  Serial.println("r");
  Serial.readBytes(listCommandBytes, serialCountByte);
    switch (listCommandBytes[0]){
      case 0: // Очистка экрана
      clearScreen();
      Serial.println("d");
      break;
      case 1: //первый экран
      takeScreen(1);
      Serial.println("d");
      break;
      case 2: //Второй экран
      takeScreen(2);
      Serial.println("d");
      break;
      case 3: //Третий экран
      takeScreen(3);
      Serial.println("d");
      break;
      case 4: //Четвертый экран
      takeScreen(4);
      Serial.println("d");
      break;
      case 5: // Устоновка символа.
      GoToPos(int(listCommandBytes[1]));
      numSymbol(int(listCommandBytes[2]));
      setSymbol();
      Serial.println("d");
      break;
      case 6: //Устоновка множества слов по адрессу
      GoToPos(int(listCommandBytes[1]));
      for (int letter=2;letter<serialCountByte;letter++){
        numSymbol(listCommandBytes[letter]);
        setSymbol();
        nextRow();
        nowPosCursor++;
      }
      Serial.println("d");
      break;
      case 7:
      gotoStart(HIGH,HIGH);
      nowPosCursor=0;
      Serial.println("d");
      break;
      
     }
}



void GoToPos(int positionNeed){
  Serial.println("s");
  while(positionNeed < nowPosCursor){
    if (nowPosCursor>60){
      gotoStart(HIGH,HIGH);
      nowPosCursor = 0;
      
      }else{
        forwardRow();
        nowPosCursor--;
        
      }
      
//      if((nowPosCursor-positionNeed)>40){
//        gotoStart(HIGH,HIGH);
//        nowPosCursor = 0;
//      } else {
//        
//      }
    }
while(positionNeed>nowPosCursor){
    if(((positionNeed-nowPosCursor)/16)>0){
        for(int tenCount = (positionNeed-nowPosCursor)/16;tenCount>0;tenCount--){
          RowAddTen();
          nowPosCursor+=16;
        }
      } else {
        nextRow();
        nowPosCursor++;
      }
    }
  
}



void nextRow(){
  digitalWrite(var6B,LOW);
  delayMicroseconds(1);
  digitalWrite(var6B,HIGH);
  delayMicroseconds(2);
  }

void forwardRow(){
  digitalWrite(var6A,LOW);
  delayMicroseconds(1);
  digitalWrite(var6A,HIGH);
  delayMicroseconds(2);
}

void RowAddTen(){
  digitalWrite(var15B,LOW);
  delayMicroseconds(1);
  digitalWrite(var15B,HIGH);
  delayMicroseconds(2);

}


void takeScreen(byte screen){
  switch(screen){
    case 1:
    digitalWrite(var2A,LOW);
    digitalWrite(var2B,LOW);
    break;
    case 2:
    digitalWrite(var2A,LOW);
    digitalWrite(var2B,HIGH);
    break;
    case 3:
    digitalWrite(var2A,HIGH);
    digitalWrite(var2B,LOW);
    break;
    case 4:
    digitalWrite(var2A,HIGH);
    digitalWrite(var2B,HIGH);
    break;
    default:
    digitalWrite(var2A,LOW);
    digitalWrite(var2B,LOW);
    }
}


void gotoStart(bool row,bool col){
  digitalWrite(var10A,row);
  digitalWrite(var12A,col);
  delay(100);
  digitalWrite(var10A,LOW);
  digitalWrite(var12A,LOW);
}


//установка символа 


void setCursor(bool statusBool){
  if (statusBool){
  digitalWrite(var8A, HIGH);
  } else {
  digitalWrite(var8A, LOW);  
  } 
}

void clearScreen(){
  digitalWrite(var18A, LOW);
  delay(20); // ровно 20???
  digitalWrite(var18A, HIGH);
  delay(3);
  
}



//устоновка символа по номеру
void takeSymbol(bool i0, bool i1, bool i2, bool i3, bool i4, bool i5, bool i6) {
  //Serial.println("Set symbol");
  digitalWrite(var22A, i6);
  digitalWrite(var22B, i5);
  digitalWrite(var20B, i4);
  digitalWrite(var24A, i3);
  digitalWrite(var23B, i2);
  digitalWrite(var18B, i1);
  digitalWrite(var24B, i0);
  delayMicroseconds(5); 
}
void setSymbol(){
  digitalWrite(var16B, HIGH);
  delayMicroseconds(1); 
  digitalWrite(var16B, LOW);
  delayMicroseconds(1);
  digitalWrite(var16B, HIGH);
  delayMicroseconds(5);
  
}


//ну тут и так все понятно....
void numSymbol(int inputdex) {
  switch (inputdex) {
  case 1: //П
    takeSymbol(0, 0, 0, 1, 1, 1, 1);
    break;
  case 2://Я
    takeSymbol(0, 0, 0, 1, 1, 1, 0);
    break;
  case 3://Р
    takeSymbol(0, 0, 0, 1, 1, 0, 1);
    break;
  case 4://С
    takeSymbol(0, 0, 0, 1, 1, 0, 0);
    break;
  case 5://Т
    takeSymbol(0, 0, 0, 1, 0, 1, 1);
    break;
  case 6://У
    takeSymbol(0, 0, 0, 1, 0, 1, 0);
    break;
  case 7://Ж
    takeSymbol(0, 0, 0, 1, 0, 0, 1);
    break;
  case 8://В
    takeSymbol(0, 0, 0, 1, 0, 0, 0);
    break;
  case 9://Ь
    takeSymbol(0, 0, 0, 0, 1, 1, 1);
    break;
  case 10://Ы
    takeSymbol(0, 0, 0, 0, 1, 1, 0);
    break;
  case 11://З
    takeSymbol(0, 0, 0, 0, 1, 0, 1);
    break;
  case 12://Ш
    takeSymbol(0, 0, 0, 0, 1, 0, 0);
    break;
  case 13://Э
    takeSymbol(0, 0, 0, 0, 0, 1, 1);
    break;
  case 14://Щ
    takeSymbol(0, 0, 0, 0, 0, 1, 0);
    break;
  case 15://Ч
    takeSymbol(0, 0, 0, 0, 0, 0, 1);
    break;
  case 16://Ю
    takeSymbol(0, 0, 1, 1, 1, 1, 1);
    break;
  case 17://А
    takeSymbol(0, 0, 1, 1, 1, 1, 0);
    break;
  case 18://Б
    takeSymbol(0, 0, 1, 1, 1, 0, 1);
    break;
  case 19://Ц
    takeSymbol(0, 0, 1, 1, 1, 0, 0);
    break;
  case 20://Д
    takeSymbol(0, 0, 1, 1, 0, 1, 1);
    break;
  case 21://Е
    takeSymbol(0, 0, 1, 1, 0, 1, 0);
    break;
  case 22://Ф
    takeSymbol(0, 0, 1, 1, 0, 0, 1);
    break;
  case 23://Г
    takeSymbol(0, 0, 1, 1, 0, 0, 0);
    break;
  case 24://Х
    takeSymbol(0, 0, 1, 0, 1, 1, 1);
    break;
  case 25://И
    takeSymbol(0, 0, 1, 0, 1, 1, 0);
    break;
  case 26://Й
    takeSymbol(0, 0, 1, 0, 1, 0, 1);
    break;
  case 27://К
    takeSymbol(0, 0, 1, 0, 1, 0, 0);
    break;
  case 28://Л
    takeSymbol(0, 0, 1, 0, 0, 1, 1);
    break;
  case 29://М
    takeSymbol(0, 0, 1, 0, 0, 1, 0);
    break;
  case 30://Н
    takeSymbol(0, 0, 1, 0, 0, 0, 1);
    break;
  case 31://О
    takeSymbol(0, 0, 1, 0, 0, 0, 0);
    break;
  case 32://P
    takeSymbol(0, 1, 0, 1, 1, 1, 1);
    break;
  case 33://Q
    takeSymbol(0, 1, 0, 1, 1, 1, 0);
    break;
  case 34://R
    takeSymbol(0, 1, 0, 1, 1, 0, 1);
    break;
  case 35://S
    takeSymbol(0, 1, 0, 1, 1, 0, 0);
    break;
  case 36://T
    takeSymbol(0, 1, 0, 1, 0, 1, 1);
    break;
  case 37://U
    takeSymbol(0, 1, 0, 1, 0, 1, 0);
    break;
  case 38://V
    takeSymbol(0, 1, 0, 1, 0, 0, 1);
    break;
  case 39://W
    takeSymbol(0, 1, 0, 1, 0, 0, 0);
    break;
  case 40://X
    takeSymbol(0, 1, 0, 0, 1, 1, 1);
    break;
  case 41://Y
    takeSymbol(0, 1, 0, 0, 1, 1, 0);
    break;
  case 42://Z
    takeSymbol(0, 1, 0, 0, 1, 0, 1);
    break;
  case 43://[
    takeSymbol(0, 1, 0, 0, 1, 0, 0);
    break;
  case 44://]
    takeSymbol(0, 1, 0, 0, 0, 1, 1);
    break;
  case 45://]
    takeSymbol(0, 1, 0, 0, 0, 1, 0);
    break;
  case 46://^
    takeSymbol(0, 1, 0, 0, 0, 0, 1);
    break;
  case 47://-
    takeSymbol(0, 1, 0, 0, 0, 0, 0);
    break;
  case 48://$
    takeSymbol(0, 1, 1, 1, 1, 1, 1);
    break;
  case 49://A
    takeSymbol(0, 1, 1, 1, 1, 1, 0);
    break;
  case 50://B
    takeSymbol(0, 1, 1, 1, 1, 0, 1);
    break;
  case 51://C
    takeSymbol(0, 1, 1, 1, 1, 0, 0);
    break;
  case 52://D
    takeSymbol(0, 1, 1, 1, 0, 1, 1);
    break;
  case 53://E
    takeSymbol(0, 1, 1, 1, 0, 1, 0);
    break;
  case 54://F
    takeSymbol(0, 1, 1, 1, 0, 0, 1);
    break;
  case 55://G
    takeSymbol(0, 1, 1, 1, 0, 0, 0);
    break;
  case 56://H
    takeSymbol(0, 1, 1, 0, 1, 1, 1);
    break;
  case 57://I
    takeSymbol(0, 1, 1, 0, 1, 1, 0);
    break;
  case 58://J
    takeSymbol(0, 1, 1, 0, 1, 0, 1);
    break;
  case 59://K
    takeSymbol(0, 1, 1, 0, 1, 0, 0);
    break;
  case 60://L
    takeSymbol(0, 1, 1, 0, 0, 1, 1);
    break;
  case 61://M
    takeSymbol(0, 1, 1, 0, 0, 1, 0);
    break;
  case 62://N
    takeSymbol(0, 1, 1, 0, 0, 0, 1);
    break;
  case 63://O
    takeSymbol(0, 1, 1, 0, 0, 0, 0);
    break;
  case 64://0
    takeSymbol(1, 0, 0, 1, 1, 1, 1);
    break;
  case 65://1
    takeSymbol(1, 0, 0, 1, 1, 1, 0);
    break;
  case 66://2
    takeSymbol(1, 0, 0, 1, 1, 0, 1);
    break;
  case 67://3
    takeSymbol(1, 0, 0, 1, 1, 0, 0);
    break;
  case 68://4
    takeSymbol(1, 0, 0, 1, 0, 1, 1);
    break;
  case 69://5
    takeSymbol(1, 0, 0, 1, 0, 1, 0);
    break;
  case 70://6
    takeSymbol(1, 0, 0, 1, 0, 0, 1);
    break;
  case 71://7
    takeSymbol(1, 0, 0, 1, 0, 0, 0);
    break;
  case 72://8
    takeSymbol(1, 0, 0, 0, 1, 1, 1);
    break;
  case 73://9
    takeSymbol(1, 0, 0, 0, 1, 1, 0);
    break;
  case 74://:
    takeSymbol(1, 0, 0, 0, 1, 0, 1);
    break;
  case 75://;
    takeSymbol(1, 0, 0, 0, 1, 0, 0);
    break;
  case 76://<
    takeSymbol(1, 0, 0, 0, 0, 1, 1);
    break;
  case 77://=
    takeSymbol(1, 0, 0, 0, 0, 1, 0);
    break;
  case 78://>
    takeSymbol(1, 0, 0, 0, 0, 0, 1);
    break;
  case 79://?
    takeSymbol(1, 0, 0, 0, 0, 0, 0);
    break;
  case 80://ПРОБЕЛ
    takeSymbol(1, 0, 1, 1, 1, 1, 1);
    break;
  case 81://!
    takeSymbol(1, 0, 1, 1, 1, 1, 0);
    break;
  case 82://"
    takeSymbol(1, 0, 1, 1, 1, 0, 1);
    break;
  case 83://#
    takeSymbol(1, 0, 1, 1, 1, 0, 0);
    break;
  case 84://@ ИЛИ 101 1011
    takeSymbol(1, 0, 1, 1, 0, 1, 1);
    break;
  case 85://%
    takeSymbol(1, 0, 1, 1, 0, 1, 0);
    break;
  case 86://&
    takeSymbol(1, 0, 1, 1, 0, 0, 1);
    break;
  case 87://'
    takeSymbol(1, 0, 1, 1, 0, 0, 0);
    break;
  case 88://(
    takeSymbol(1, 0, 1, 0, 1, 1, 1);
    break;
  case 89://)
    takeSymbol(1, 0, 1, 0, 1, 1, 0);
    break;
  case 90://*
    takeSymbol(1, 0, 1, 0, 1, 0, 1);
    break;
  case 91://+
    takeSymbol(1, 0, 1, 0, 1, 0, 0);
    break ;
  case 92://,
    takeSymbol(1, 0, 1, 0, 0, 1, 1);
    break;
  case 93://-
    takeSymbol(1, 0, 1, 0, 0, 1, 0);
    break;
  case 94://.
    takeSymbol(1, 0, 1, 0, 0, 0, 1);
    break;
  case 95://ПАЛКА СУКА
    takeSymbol(1, 0, 1, 0, 0, 0, 0);
    break;
  case 0: // спец символ
    takeSymbol(0, 0, 0, 0, 0, 0, 0);
    break;

  //default:
    
  }
}
