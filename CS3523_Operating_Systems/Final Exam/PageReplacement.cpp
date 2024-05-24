# include <iostream>
# include <fstream>
# include <queue>
# include <vector>

using namespace std;

// function declarations
int FIFO(vector<int>, int);
int LRU(vector<int>, int);
int OPT(vector<int>, int);



int main()
{

    string input_file = "input.txt";

    ifstream indata;
    indata.open(input_file);

    // if file cannot be opened, return error
    if(!indata){
        cout<< "Error: File not Found!" << endl;
        return 0;
    }

    // retrieve data for number of frames and page size
    int N , pagesize;

    indata >> N >> pagesize;

    vector<int> address{};

    int a;


    while(true)
    {   
        indata >> a;
        if(a == -1) break;
        address.push_back(a / pagesize);
    }
    
    // closing the input file
    indata.close(); 

    // printing output
    printf("The number of page faults with FIFO is %d\n" , FIFO(address , N));
    printf("The number of page faults with LRU is %d\n" , LRU(address , N));
    printf("The number of page faults with OPT is %d\n" , OPT(address , N));

    return 0;
}

// ------------- FIFO -----------------
int FIFO(vector <int> address, int N)
{

    int faults = 0;
    int size_queue = 0;
    vector <int> current;
    queue <int> q;

    for(int i = 0 ; i < address.size() ; i++)
    {           
        // if it is not the first reference
        if(i != 0)
        {
            bool in_queue = false;

            // first check if its there in the queue
            for(int s = 0 ; s < current.size() ; s++)
            {   
                if(current[s] == address[i])
                {   
                    // printf("Already there in queue\n");
                    in_queue = true; 
                    break;
                }
            }

            // if its not in the queue
            if(!in_queue)
            {
                // if queue_size = number of frames
                if(size_queue == N)
                {
                    // remove first element
                    int remove = q.front();
                    q.pop();
                    q.push(address[i]);

                    // find the element "remove" and set it to -1
                    for(int s = 0 ; s < current.size() ; s++)
                    {   
                        if(current[s] == remove)
                        {   
                            // printf("Removing %d\n",remove);
                            current[s] = -1;
                            break;
                        }
                    }
                    // increment the number of faults
                    faults++;

                    // add it to the current list of items in stack
                    current.push_back(address[i]);
                }

                // if the queue has not reached its limit, simply add the element to the queue
                else
                {
                    q.push(address[i]);
                    faults++;
                    size_queue++;
                    current.push_back(address[i]);
                }
            }
        }

        // if it is the first address reference
        if(i == 0)
        {   
            // will always be a fault
            faults++;

            // adding to the queue
            size_queue++;
            q.push(address[i]);

            // adding it to the current elements in the queue
            current.push_back(address[i]);
        }
    }

return faults;
}


// ------------- LRU -----------------
int LRU(vector <int> address, int N)
{
    int frames[N];
    int frames_occupied = 0;
    int last_references[N];
    int faults = 0;

    // we initialize all the frames to -1
    for(int i = 0 ; i < N ; i++) frames[i] = -1;

    for(int i = 0 ; i < address.size() ; i++)
    {   

        // printf("CURRENT FRAMES %d %d %d" , frames[0] , frames[1] , frames[2])

        // if it is not the first address reference
        if(i != 0)
        {
            // we first check if its already there in the frames
            bool in_frames = false;

            for(int s = 0 ; s < N ; s++)
            {
                if(frames[s] == address[i])
                {
                    in_frames = true;
                    last_references[s] = i;
                    break;
                }
            }
    
            // if not in frames, we check if all N frames are occupied
            if(!in_frames)
            {
                if(frames_occupied == N)
                {
                    // we find the least last reference and replace the element
                    int least_max_refer = 1e8;
                    int index_to_replace = -1;

                    for(int s = 0 ; s < N ; s++)
                    {
                        if(last_references[s] < least_max_refer)
                        {
                            index_to_replace = s;
                            least_max_refer = last_references[s];
                        }
                    }

                    frames[index_to_replace] = address[i];
                    last_references[index_to_replace] = i;

                    // we increment the number of faults
                    faults++;
                }


                // we just add it to the frames
                else
                {
                    frames[frames_occupied] = address[i];
                    last_references[frames_occupied] = i;
                    frames_occupied++;
                    faults++;
                }
            }    
        }

        // it is the first address reference
        else
        {   
            // we add it to the frames and by default its a fault
            frames[frames_occupied] = address[i];
            last_references[frames_occupied] = i;
            faults++;
        }
    }
    return faults;

}

// ------------- OPT -----------------
int OPT(vector <int> address, int N)
{
    int frames[N];
    int frames_occupied = 0;
    int faults = 0;

    // we initialize all the frames to -1
    for(int i = 0 ; i < N ; i++) frames[i] = -1;

    for(int i = 0 ; i < address.size() ; i++)
    {   
        // if it is not the first address reference
        if(i != 0)
        {
            // we first check if its already there in the frames
            bool in_frames = false;

            for(int s = 0 ; s < N ; s++)
            {
                if(frames[s] == address[i])
                {
                    in_frames = true;
                    break;
                }
            }
    
            // if not in frames, we check if all N frames are occupied
            if(!in_frames)
            {
                if(frames_occupied == N)
                {
                    // we check for the next reference for all pages in frames
                    int next_references[N];

                    // we initialize this array to large values
                    for(int s = 0 ; s < N ; s++) next_references[s] = 1e7;

                    for (int elem = 0 ; elem < N ; elem++)
                    {
                        // we wish to check if frames[elem] has a next reference
                        for(int s = i+1 ; s < address.size() ; s++)
                        {   
                            if (frames[elem] == address[s])
                            {
                               next_references[elem] = s;
                                break;
                            }
                        }
                    }

                    // we check for victim page, that will not be referenced for longest time
                    int max_ref = -1e6;
                    int index_to_replace = -1;
                    for(int s = 0 ; s < N ; s++)
                    {
                        if (next_references[s] > max_ref)
                        {
                            max_ref = next_references[s];
                            index_to_replace = s;
                        }
                    }

                    // replacing the frame
                    frames[index_to_replace] = address[i];
                    faults++;
                }

                // we just add it to the frames
                else
                {
                    frames[frames_occupied] = address[i];
                    frames_occupied++;
                    faults++;
                }
            }    
        }

        // it is the first address reference
        else
        {   
            // we add it to the frames and by default its a fault
            frames[frames_occupied] = address[i];
            frames_occupied++;
            faults++;
        }
    }
    return faults;
}

