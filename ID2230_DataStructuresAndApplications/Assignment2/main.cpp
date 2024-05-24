/*************************************************************
ID2230

AUTHOR: TANMAY GOYAL, AI20BTECH11021

ASSIGNMENT 2: USER AUTHENTICATION

NOTE: code is running fine on replit.com and on a MacOSX System (Anything that runs clang)
**************************************************************/


#include <iostream>
#include <fstream>
#include <cstring>
#include <cmath>

using namespace std;

long long hash_key(string username)
{
    /*
    computes the hash key of a given username, by converting the username into 
    its equivalent number with base 2, and then taking a moduli with 20000. We would
    use linear probing to address collisions.
    
    The idea was to take base 26, but wasn't done due to fear of overflow.
    */
    
    long long key = 0;

    for (int i =0 ; i<username.length() ; i++)
    {
        key += int(username[i])*pow(2,username.length()-i-1);
    }
    key = key % 20000;
    return key;
}


int main()
{
    string hashtable[20000][2];// the hashtable

    // initialising all entries to 'x'
    for (int i = 0 ; i<20000 ; i++)
    {
        for (int j =0 ; j<2 ; j++)
        {
            hashtable[i][j] = "x";
        }
    }

    string line;
    ifstream fin;
    int count = 0;

    //reading the file
    fin.open("userInfo.csv");

    while(getline(fin,line))
    // while we are still able to read data from fin into line
    {
        string username = "";
        string password = "";
        // splitting about the comma into username and password

        int i =0 ;
        for (; line[i]!=',';i++)
        {
            username += line[i];
        }
        
        i += 1;

        for(;i < line.length()-1 ; i++)
        // length-1 to avoid the extra space at the end of password
        {
            password += line[i];
        }

        long long k = hash_key(username);// calculating the hash key
        
        bool entry_success = false;

        while(!entry_success) //linear probing to resolve collisions
        {
            if (hashtable[k][0] != "x") // not an empty position in the hash table
            {
               
                if(k == 19999) //reached the end of indices
                {
                    k = 0;
                }
                else
                {
                    k += 1; // we check if the next slot is empty
                }
            }
            else
            {// empty position found
                hashtable[k][0] = username;
                hashtable[k][1] = password;
                entry_success = true;


            }
        }
    }
    
    string prompted_username ;
    string prompted_password;
    // to avoid two iterations through hash_table, we would store the 
    //actual password as soon as we find a match for the valid username
    string actual_password;

    cout<<"Enter username: "<<endl;
    cin>>prompted_username;

    long long k = hash_key(prompted_username);
    
    long long i = k;
  // introduce an iterator through the table, so we can check when i becomes equal to k
  // and to avoid infinite loops through table
    bool found = false;

    while(!found)
    {
      if(hashtable[i][0]==prompted_username)
      {
        found = true;
        actual_password = hashtable[i][1];
      }
      else
      {
        bool key_change = false; // to check if the key got incremented or not
        if (i == 19999)// end of indices
        {
            i = 0;
            key_change = true;
        }
        
        if(i == k-1){break;}// its going to start a second iteration over the table
        
        if(!key_change){i+=1;}
      }
    }
    // doing the authentication
    if (found == false) // username was invalid
    {
        cout<<"Name not found"<<endl;
    }
    else
    {
        cout<<"Enter password: "<<endl;
        cin>>prompted_password;
        if (prompted_password == actual_password) // if password is correct
        {
            cout<< "Login successful"<< endl;
        }
        else    // incorrect password
        {
            cout<<"Incorrect password"<<endl;
        }
    }

    return 0;

} 
    

