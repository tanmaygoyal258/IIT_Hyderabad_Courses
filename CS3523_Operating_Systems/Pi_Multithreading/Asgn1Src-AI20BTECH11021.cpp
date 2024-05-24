// importing required libraries
# include <iostream>
# include <fstream>
# include <math.h>
# include <pthread.h>

using namespace std;

// function declaration
void* thread_within_circle(void* point);

// defining a class to hold cartesian points
class XY_point{
    private:
        // x coordinate
        float x;

        // y coordinate
        float y;

        // thread number
        int thread_num;

        // whether point is within the circle or not
        int within_circle;

    public:
        // constructor
        XY_point(float x , float y , int t , int within) : 
        x(x) , y(y) , thread_num(t) , within_circle(within) {}

        // function to get x-coordinate
        float get_x(){return this-> x;}

        // function to get y-coordinate
        float get_y(){return this->y;}  

        // function to get thread number
        float get_thread_num(){return this->thread_num;}  

        // function to get whether point is within circle or not
        int get_within_circle(){return this->within_circle;}
};

// global variable to hold starting points for each thread assuming there will be no more than 100 threads
int starts[100];

// global variable to hold number of points within circle for each thread assuming there will be no more than 100 threads
int points_in_circle[100];

int main(){

    // name of input file
    string input_file_name = "input.txt";

    // opening input file
    ifstream indata;
    indata.open(input_file_name);

    // if file cannot be opened, return error
    if(!indata){
        cout<< "Error: File not Found!" << endl;
        return 0;
    }

    // retrieve data for number of threads and number of points
    int num_points , num_threads;
    indata >> num_points >> num_threads;

    // closing the input file
    indata.close(); 

    // calculating number of points for each thread and the extra points left
    int points_per_thread = num_points / num_threads;
    int extra_points = num_points % num_threads;

    // index of point processed by last thread
    int last_seen = -1;

    // calculating starting points for each thread
    for(int i = 0 ; i < num_threads ; i++){
        // starting poijnt for a thread is the next point after the last one processed
        starts[i] = last_seen + 1;

        // updating the last seen point
        last_seen += points_per_thread;
        if(i < extra_points) last_seen++;
    }
    // adding an extra element to the array for the last point for convinience
    starts[num_threads] = num_points;

    /*
    making a 2D array to hold randomly generated points
    number of rows = nunber of threads
    each row contains appropriate number of points
    advantage of the 2D array is we can directly pass it to the thread function
    instead of creating a seperate array for every thread again
    there is one extra slot at the beginning of each row containing dummy point
    the purpose of this point is to convey the thread number to the thread func
    */ 
    XY_point** random_points = (XY_point**) malloc(num_threads * sizeof(XY_point*));

    for(int i = 0 ; i < num_threads ; i++){

        // +1 indicates the dummy point
        random_points[i] = (XY_point*) malloc((starts[i+1] - starts[i] + 1) * sizeof(XY_point));
        
        // creating the dummy point
        random_points[i][0] = XY_point(0 , 0 , i , 0);
    }


    // allows for the seed of rand to change every time the program is run
    srand(time(0));

    // creating an array of thread_ids
    pthread_t t_id[num_threads];

    // starting the timer
    auto start_time = std::chrono::high_resolution_clock::now();    

    // creating the threads
    for(int t = 0 ; t < num_threads ; t++)
        pthread_create(&t_id[t] , NULL , thread_within_circle , random_points[t]);

    // waiting for all threads to finish
    for(int t = 0 ; t < num_threads ; t++)
        pthread_join(t_id[t] , NULL);   

    // ending the timer
    auto end_time = std::chrono::high_resolution_clock::now();

    // total number of points within the circle from all threads
    int total_within = 0;

    for(int i = 0 ; i < num_threads ; i++) total_within += points_in_circle[i];

    // calculating the value of pi
    float pi = 4 * (float) total_within / num_points;

    // calculating the time taken for creation of threads and the thread processes
    float time_elapsed = std::chrono::duration_cast<std::chrono::microseconds>(end_time - start_time).count();

    // opening the output file
    ofstream outdata;
    outdata.open("output.txt");

    // if file cannot be opened, return error
    if(!outdata){
        cout<<"Error: Cannot open file!";
        return 0;
    }

    // writing in the output to the file
    outdata << "Number of Points: " << num_points << endl;
    outdata << "Number of Threads: " << num_threads << endl;
    outdata << "Time: " << time_elapsed << " microseconds" << endl;
    outdata << "Value of Pi Computed: " << pi << endl;
    
    for(int i = 0 ; i < num_threads ; i++){

        // writing to the file
        outdata << "\n" << endl;
        
        outdata << "Thread " << i + 1 << " : Number of points within square = " 
        << starts[i+1] - starts[i] << " , Number of points within circle = " 
        << points_in_circle[i] << endl;

        outdata << "\nPoints within circle: ";

        // we start from 1 becuase index 0 has the dummy point
        for(int j = 1; j < starts[i+1] - starts[i] ; j++){
            if(random_points[i][j].get_within_circle() == 1){
                outdata << "(" << random_points[i][j].get_x() << " , " 
                << random_points[i][j].get_y() << "), ";
            }
        }

        // we start from 1 becuase index 0 has the dummy point
        outdata << "\nPoints within square: ";
        for(int j = 1 ; j < starts[i+1] - starts[i] ; j++){
            if(random_points[i][j].get_within_circle() == 0){
                outdata << "(" << random_points[i][j].get_x() << " , " 
                << random_points[i][j].get_y() << "), ";
            }
        }

    }

    // closing the output file
    outdata.close();

    // freeing the memory
    free(random_points);

    return 0;

}


void* thread_within_circle(void* point){

    // function to check if a point is within the circle centered at origin and 
    // with unit radii or not
    
    XY_point* points = (XY_point*) point;

    // getting the thread number
    int thread_num = points[0].get_thread_num();

    // calculating the number of points the thread is responsible for
    int number_points = starts[thread_num + 1] - starts[thread_num];

    // keeping track of the number of points within the circle
    int within = 0;

    // generating the random points
    for(int i = 0 ; i < number_points ; i++){

        // generating a random float between 0 and 1    
        float x_rand = (float) rand() / RAND_MAX;
        float y_rand = (float) rand() / RAND_MAX;

        
        // converting the random floats to a point between -1 and 1 using the fact that
        // any float x between 0 and 1 can be converted to a number between a and b using the formula
        // a + (b-a) * x
        float x = 2 * x_rand - 1;
        float y = 2 * y_rand - 1;

        // to store if point is within circle or not
        int within_c;

        // checking if the point is within the circle
        if(x*x + y*y <= 1) {
            within++;

            // updating the variable if point is within the circle
            within_c = 1 ;
        }
        else within_c = 0;

        // creating the point -> (i+1) because index 0 is the dummy point
        points[i+1] = XY_point(x , y , thread_num , within_c);
    }

    // updating the global array
    points_in_circle[thread_num] = within;

    // since return type is void*
    return NULL;
}