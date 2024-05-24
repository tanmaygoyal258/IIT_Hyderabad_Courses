/*
ID2230
ASSIGNMENT 1: POSTFIX EXPRESSIONS
AUTHOR: TANMAY GOYAL, AI20BTECH11021
*/


// example inputs include 6,7,+,\n
// example inputs include 10,2,+,7,/,3,*,\n 

#include <iostream>
#include <string.h>
#include <math.h>
//#include <typeinfo>

using namespace std;

int STACK_SIZE = 500;

int isEmpty(int* index);
int isFull(int* index);
void push(double* S , double x , int* index);
double pop(double* S , int* index );
   
int main()
{
    // creating stack
    double* S = (double*)malloc(STACK_SIZE * sizeof(double));
    int index = -1;
    int* top = &index;
    
    // taking input
    char expression[1000];
    cout<<"Enter postfix expression: "<<endl;
    cin.getline(expression,1000);

    int result = 1;

    for(int i = 0 ; (expression[i]!='\\' && expression[i+1]!='n')  && result == 1 ; i++){
        // since our last character 6,is \n, we introduce the condition to check that
        
        if(expression[i]==' ' || expression[i]==',')
         // checking for white spaces and/or commas, we continue to the next token
        {
            continue;
        }
        
        // checking for operator (for negative sign, make sure it is not a negative number)
        // we do this by checking if next char is comma, or if it is the end of the line (which is \n)
        else if(expression[i]=='+' || (expression[i]=='-' && (expression[i+1] == ','||(expression[i+1] == '\\' && expression[i+2] == 'n')))||expression[i]=='*'||expression[i]=='/' )
        {
            double a  = pop(S , top);
            double b = pop(S , top);
            // checking for validity
            if( a==INT_MIN || b==INT_MIN)
            {
                cout<<"Invalid Expression"<<endl;
                result = -1;
                break;
            }
            else
            {
                if(expression[i]=='+'){push(S , b+a , top);}
                if(expression[i]=='-'){push(S , b-a , top);}
                if(expression[i]=='*'){push(S , b*a , top);}
                if(expression[i]=='/' && a!=0){push(S , b/a , top);}
                if(expression[i]=='/' && a ==0){cout<<"Division by Zero error"<<endl;}
            }
            
        }

        // check for negative number
        else if (expression[i]=='-') 
        {
        // it will be a number -> if number has more than 1 digit, it needs to be taken into account
            int digits = 0;
            int j = i+1; // since ith position had the minus sign
            int face_value[10]; //assuming no number is greater than 10^10
            while(expression[j] != ',')
            {
                //cout << typeid(expression[j]).name() << endl;
                face_value[digits] = expression[j] - '0'; //converting char to int
                //cout<<digits<<face_value[digits]<<endl;
                digits ++;
                j++;
            }
            
            double number = 0;
            for(int k = 0 ; digits>=1 ; k++ , digits--)
            {// reconstructing the number
                number += face_value[k] * pow(10,digits-1);
            }
            push(S , (-1*number) , top);
            i = j;
        }
        
        // it will be a number -> if number has more than 1 digit, it needs to be taken into account
        else 
        {
            int digits = 0;
            int j = i;
            int face_value[10]; //assuming no number is greater than 10^10
            while(expression[j] != ',')
            {
                // keeping track of number of digits to help reconstruct number

                //cout << typeid(expression[j]).name() << endl;
                face_value[digits] = expression[j] - '0'; //converting char to int
                //cout<<digits<<face_value[digits]<<endl;
                digits ++;
                j++;
            }
            
            double number = 0;
            for(int k = 0 ; digits>=1 ; k++ , digits--)
            {
                // reconstructing the number
                number += face_value[k] * pow(10,digits-1);
            }
            push(S , number , top);
            i = j;
        }

    }

    if(index==0)
    {
        double result = pop(S , top);
        cout<<result<<endl;
    }
    else
    {
        cout<<"Invalid Expression"<<endl;
    }
    
    return 0;
}


//Functions

int isEmpty(int* index)
{
    return (*index)<0;
}

int isFull(int* index)
{
    return (*index)==STACK_SIZE - 1;
}

void push(double* S , double x , int* index)
{
        if(isFull(index))
        {
            printf("Stack is full");
        }
        else
        {
            (*index) += 1;
            S[*index] = x;
        }
}

double pop(double* S , int* index )
{
    if(isEmpty(index))
    {
        printf("Stack is Empty");
        return INT_MIN;
    }
    else
    {
        double var = S[*index];
        (*index)-=1;
        return var;
    }
}

