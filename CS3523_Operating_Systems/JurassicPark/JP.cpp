// importing required libraries
# include <iostream>
# include <unistd.h>
# include <chrono>
# include <cstring>
# include <pthread.h>
# include <random>
# include <atomic>
# include <deque>
# include <fstream>
# include <semaphore.h>
# include <mutex>

using namespace std;

// defining the semaphores
sem_t emptyCars;            // counting semaphore keeping track of the number of empty cars
sem_t passengerLine;        // binary semaphore to keep track of the front of the passenger line
sem_t totalNumberRides;     // binary semaphore to allow only one thread to update the total number of rides
sem_t* occupiedCar;         // array of binary semaphores for each car to indicate it is occupied
sem_t carLineUpdate;        // binary sempahore to allow only one car thread to update the carLine

// defining an array for car status
int* carStatus;     // -1 indicates free, -5 indicates unavailable, >0 indicates passenger number

// keeping a counter for the total number of rides done
atomic <int> num_rides_done {0};

// defining a double ended queue which shall track the first in line of cars to be ready
deque<int> carLine;

// creating a class for parameters to be passed to passengers
class passenger_params
{
    public:
    int passenger_num;      // index of the passenger 
    int total_requests;     // total number of requests per passenger
    int car_nums;           // total number of cars available
    int lambda_p;           // exponential distribution parameter for time between two requests
    FILE* f;                // pointer to the output file

    // defining the constructor
    passenger_params(int passenger_num , int total_requests , int car_nums , int lambda_p , FILE* f):
        passenger_num(passenger_num) , total_requests(total_requests) , car_nums(car_nums) , lambda_p(lambda_p) , f(f) {}
};

// creating a class for parameters to be passed to cars
class car_params
{
    public:
    int car_num;            // index of the car
    int lambda_c;           // exponential distribution parameter for time between two rides
    int total_rides;        // total number of rides to be done
    FILE* f;                // pointer to the output files

    // defining the constructor
    car_params(int car_num , int lambda_c , int total_rides, FILE* f):
        car_num(car_num) , lambda_c(lambda_c) , total_rides(total_rides) , f(f) {}
};

// function initializations
string get_time();
void* passenger(void* params);
void* car(void* params);

int main()
{   
    // defining the variables
    int num_pass , num_cars , num_requests;
    double lambda_p , lambda_c;

    // name of input file
    string input_file = "inp-params.txt";

    // opening the input file
    ifstream indata;
    indata.open(input_file);

    // If the file does not exist, return error
    if(!indata){
        cout << "Error! File not found." << endl;
        return 0;
    }

    // obtaining the parameters
    indata >> num_pass >> num_cars >> lambda_p >> lambda_c >> num_requests;
    
    // closing the input file
    indata.close();
    // opening the output file
    FILE *f = fopen("output.txt" , "w");

    // if the file cannot be opened, return error
    if (!f){
        cout << "Error! File cannot be opened." << endl;
        return 0;
    }

    // printing the title
    fprintf(f , "Jurrasic Park Problem with %d passengers, %d cars, and %d requests per passenger\n\n" , 
    num_pass , num_cars , num_requests);

    // creating the parametres for the passenger and car threads
    passenger_params* passenger_parameters = (passenger_params*) malloc(num_pass * sizeof(passenger_params));
    car_params* car_parameters = (car_params*) malloc(num_cars * sizeof(car_params));

    // car parameters
    for(int i = 0 ; i < num_pass ; i++) 
        passenger_parameters[i] = passenger_params(i+1 , num_requests , num_cars , lambda_p , f);

    // passenger parameters
    for(int i = 0 ; i < num_cars ; i++)
        car_parameters[i] = car_params(i , lambda_c , num_pass * num_requests , f);

    //initializing the semaphores
    sem_init(&emptyCars , 0 , 0);           // none of the cars are available, cars would signal once ready
    sem_init(&passengerLine , 0 , 1);
    sem_init(&totalNumberRides , 0 , 1);
    sem_init(&carLineUpdate , 0 , 1);

    // initialising the array of semaphores for occupiedCars to 0, 
    // each car shall signal the sempahore once its ready
    occupiedCar = new sem_t[num_cars];
    for(int i = 0; i < num_cars ; i++) sem_init(&occupiedCar[i] , 0 , 0 );

    // initializing the car status array
    carStatus = new int[num_cars];
    for(int i = 0 ;+ i < num_cars ; i++)
        carStatus[i] = -5;      // -5 indicates car is unavailable, whereas -1 indicates car is free

    // creating the threads
    pthread_t car_id[num_cars];
    pthread_t passenger_id[num_pass];

    // starting the timer from when the process beings to simulate
    auto start_time = chrono::high_resolution_clock::now();

    // car threads
    for(int i = 0 ; i < num_cars ; i++)
        pthread_create(&car_id[i] , NULL , car , &car_parameters[i]);

    // passenger threads
    for(int i = 0 ; i < num_pass ; i++)
        pthread_create(&passenger_id[i] , NULL , passenger , &passenger_parameters[i]);

    // joining the car threads
    for(int i = 0 ; i < num_cars ; i++)
        pthread_join(car_id[i] , NULL);
    
    // joining the passenger threads
    for(int i = 0 ; i < num_pass ; i++)
        pthread_join(passenger_id[i] , NULL);
    
    // ending the timer
    auto end_time = chrono::high_resolution_clock::now();

    // calculating the time elapsed
    float time_elapsed = chrono::duration_cast<chrono::microseconds>(end_time - start_time).count();

    // printing the time elapsed to the ouptut file and the terminal for convinience
    fprintf(f, "\nThe time taken is %lf seconds\n" , time_elapsed / 1000000);
    cout << "Time taken = " << time_elapsed / 1000000 << " seconds" << endl;

    // destroying the semaphores
    sem_destroy(&emptyCars);
    sem_destroy(&passengerLine);
    sem_destroy(&totalNumberRides);
    sem_destroy(&carLineUpdate);
    for(int i = 0 ; i < num_cars ; i++) sem_destroy(&occupiedCar[i]);

    // freeing the memory on the heap
    free(passenger_parameters);
    free(car_parameters);
    free(carStatus);
    free(occupiedCar);

    // closing the output file
    fclose(f);

    return 0;
}


string get_time()
{       
    time_t t = time(0);
    string s = ctime(&t);
    int colon = s.find(":");
    s = s.substr(colon-2 , 8);
    return s;
}


void* passenger(void* params)
{
    // converting the parameters to appropriate type
    passenger_params* p = (passenger_params*) params;

    // extracting the required parameters
    int passenger_num = p->passenger_num;
    int total_requests = p->total_requests;
    int lambda_p = p->lambda_p;
    int num_cars = p->car_nums;
    FILE* f = p->f;

    // printing to the log when passenger enters the museum
    fprintf(f , "Passenger %d enters the museum at %s\n" , passenger_num , get_time().c_str()) ;

    // each passenger makes total_requests number of requests
    for(int req = 0 ; req < total_requests ; req++)
    {
        // we let the passenger wander around for a while to create some time between two
        // successive requests.

        // defining the exponential random generator
        unsigned seed =  chrono::system_clock::now().time_since_epoch().count();
        default_random_engine generator(seed);
        exponential_distribution <double> distribution(lambda_p);
        
        // randomly letting passenger wander
        usleep(distribution(generator) * 1000000);

        // passenger is ready to get into line after wandering around
        fprintf(f , "Passenger %d has joined the line for a car at %s\n" , 
            passenger_num , get_time().c_str());

        // passenger is now in the line. If it acquires the semaphore passengerLine, 
        // it is in front of the line, so it will be served first
        sem_wait(&passengerLine);

        // variable to hold the index of the car allotted to the passsenger
        int car_index = -1;

        // till we are not able to find a suitable car to travel in for the person in front of the line
        // note that it still holds the front of the line passengerLine semaphore
        while(car_index == -1)
        {
            // Since it is in front of the line, it waits till an empty car is available 
            sem_wait(&emptyCars);

            // if carLine is not empty
            if(!carLine.empty())
            {   
                // we find the car number at the front and remove it
                // for this we acquire the semaphore carLineUpdate
                sem_wait(&carLineUpdate);
                car_index = carLine[0];
                carLine.pop_front();
                sem_post(&carLineUpdate);
                
                // we output to the log
                fprintf(f , "Passenger %d is entering car %d at %s\n" , 
                        passenger_num , car_index + 1 , get_time().c_str());
                    
                // we indicate that the car is now occupied ->
                // this will not cause any wait since the car is ready and had already signalled to the semaphore
                sem_wait(&occupiedCar[car_index]);

                // we set the carStatus to passenger_num->
                // as soon as its done, the ride shall begin
                carStatus[car_index] = passenger_num;
                                
                // since the first in line has found the car, we allow the next in line to take over
                sem_post(&passengerLine);
            }
        }

        // passenger thread busy waits till the car does not update its status to unavailable
        while(carStatus[car_index] != -5);

        // updating the time when the passenger gets off the car
        fprintf(f , "Passenger %d is getting off car %d at %s\n" , passenger_num , car_index+1 , get_time().c_str());

        // since one ride is done we increment the number of rides done
        // we make sure there is no race condition by using a 
        // semaphore to update the shared variable
        sem_wait(&totalNumberRides);
        num_rides_done++;
        sem_post(&totalNumberRides);
        // cout << num_rides_done << endl;

        // ONLY once the update for number of rides is done 
        // shall we allow the car to leave for its break
        // if this semaphore is not there, the car is ready for the next 
        // passenger even before we can make the update
        sem_post(&occupiedCar[car_index]);
    }

    // after the passenger is done with all the rides, it exits the museum
    fprintf(f , "Passenger %d is exiting the museum at %s\n" , passenger_num , get_time().c_str());
    
    // since return type is void*
    return NULL;
}


void* car(void* params)
{
    // converting the parameters to appropriate type
    car_params* p = (car_params*) params;

    // extracting the required parameters
    int car_num = p->car_num;
    int lambda_c = p->lambda_c;
    int total_rides = p->total_rides;
    FILE* f = p->f;

    // we keep all the cars running till the total number of rides are done
    while(num_rides_done <= total_rides)
    {
        // we let the car take breaks in between successive rides

        // defining the exponential random generator
        unsigned seed =  chrono::system_clock::now().time_since_epoch().count();
        default_random_engine generator(seed);
        exponential_distribution <double> distribution(lambda_c);
        
        // letting the car take a break
        usleep(distribution(generator) * 1e6);

        // once the car is available, it updates its status to -1 i.e available and free
        carStatus[car_num] = -1;

        // it establishes itself in the carLine, we acquire the sempahore for this
        sem_wait(&carLineUpdate);
        carLine.push_back(car_num);
        sem_post(&carLineUpdate);
        
        // it also signals emptyCars to let the passenger know its available
        sem_post(&emptyCars);

        // it also updates its semaphore of being occupied, and allows the passenger to get on
        sem_post(&occupiedCar[car_num]);

        // car thread busy waits till its not allotted a passenger 
        while(carStatus[car_num] == -1)
        {   
            // in case car thread starts waiting, and the total number of rides have been completed
            // its asked to exit
            if(num_rides_done == total_rides) break;
        }

        // if the total number of rides have been completed, the car thread exists the outer while loop
        if(num_rides_done == total_rides) break;
        
        // the passenger rides the car for a random time between 1 and 5 seconds
        usleep((rand() % 5 + 1) * 1e6);

        // once the ride is done, the car once again switches its status to -5 i.e unavailable
        carStatus[car_num] = -5;

        // waits on the semaphore till the passenger is not done updating the total number of rides
        // once the passenger signals, is only when the car is allowed to leave
        sem_wait(&occupiedCar[car_num]);
    }

    // since return type is void*
    return NULL;
}