# include "types.h"
# include "date.h"
# include "user.h"

void convert_UTC_to_IST(struct rtcdate *r);
int is_leap_year(uint year);


int main(void)
{
    struct rtcdate r; 

    if (mydate(&r)){
        printf(2 , "date failed\n");
        exit();
    }   
    else{
        char* month[] = {"January" , "February" , "March" , "April" , "May" , "June" , "July" , "August" , "September" , "October" , "November" , "December"};
        
        char time_UTC[] = "00:00:00";
        
        if(r.second < 10){
            time_UTC[7] = '0' + r.second;
        }
        else{
            time_UTC[6] = '0' + r.second / 10;
            time_UTC[7] = '0' + r.second % 10;
        }
        if(r.minute < 10){
            time_UTC[4] = '0' + r.minute;
        }
        else{
            time_UTC[3] = '0' + r.minute / 10;
            time_UTC[4] = '0' + r.minute % 10;
        }
        if(r.hour < 10){
            time_UTC[1] = '0' + r.hour;
        }
        else{
            time_UTC[0] = '0' + r.hour / 10;
            time_UTC[1] = '0' + r.hour % 10;
        }
        
        printf(1 , "---UTC---\n");
        printf(1 , "Year : %d\n" , r.year);
        printf(1 , "Month : %d or %s\n" , r.month , month[r.month-1]);
        printf(1 , "Date : %d\n" , r.day);
        printf(1 , "The time is %s\n" , time_UTC);

        convert_UTC_to_IST(&r);
        char time_IST[] = "00:00:00";
        
        if(r.second < 10){
            time_IST[7] = '0' + r.second;
        }
        else{
            time_IST[6] = '0' + r.second / 10;
            time_IST[7] = '0' + r.second % 10;
        }
        if(r.minute < 10){
            time_IST[4] = '0' + r.minute;
        }
        else{
            time_IST[3] = '0' + r.minute / 10;
            time_IST[4] = '0' + r.minute % 10;
        }
        if(r.hour < 10){
            time_IST[1] = '0' + r.hour;
        }
        else{
            time_IST[0] = '0' + r.hour / 10;
            time_IST[1] = '0' + r.hour % 10;
        }

        printf(1 , "---IST---\n");
        printf(1 , "Year : %d\n" , r.year);
        printf(1 , "Month : %d or %s\n" , r.month , month[r.month-1]);
        printf(1 , "Date : %d\n" , r.day);
        printf(1 , "The time is %s\n" , time_IST);


    }
    

    exit();
}

int is_leap_year(uint year){
    // if not divisible by 4 certainly not a leap year
    if (year % 4 != 0) return 0;

    // if not divisible by 100 but divisible by 4, it is a leap year
    else if (year % 4 == 0 && year % 100 != 0) return 1;

    // if divisble by 100 and 400, it is a leap year
    else if (year % 400 == 0) return 1;

    else return 0;
}

void convert_UTC_to_IST(struct rtcdate *r){

    if (r->hour >= 18 && r->minute >= 30){

        // new day according to IST and UTC = +5:30 IST        
        r->day += 1;
        r->hour += 5 - 23;
        r->minute += 30 - 60;

        // days per month in leap year and normal year
        int day_per_month_non_leap[] = {31 , 28 , 31 , 30 , 31 , 30 , 31 , 31  ,30 , 31 , 30 , 31}; 
        int day_per_month_leap[] = {31 , 29 , 31 , 30 , 31 , 30 , 31 , 31  ,30 , 31 , 30 , 31}; 

        // in case we overshot the number of days in a month in a leap year
        if(is_leap_year(r->year) && r->day > day_per_month_leap[r->month-1]){
            r->month += 1;
            r->day = 1;

            // in case we overshot to the 13th month
            if(r->month > 12){
                r->month = 1;
                r->year += 1;
            }
        }

        // in case we overshot the number of days in a month in a non-leap year
        if(r->day > day_per_month_non_leap[r->month-1]){
            r->month += 1;
            r->day = 1;

            // in case we overshot to the 13th month
            if(r->month > 12){
                r->month = 1;
                r->year += 1;
            }
        }
    }

    else{
        // UTC = +5:30 IST
        r->hour += 5;
        r->minute += 30;

        // new hour
        if(r->minute >= 60){
            r->minute -= 60;
            r->hour += 1;
        }
    }
}