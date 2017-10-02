#include <stdio.h>

__declspec(dllexport) int JulianDay(int year, int month, int day, int hour) {

    // this is the code inside of the dll file, any changes you make to this you have to recompile it as a dll again

    int ySinceBC = year + 4800 - ((14-month)/12);
    int mSinceBC = month + 12*((14-month)/12) - 3;
    
    int JDN = day + ((153*mSinceBC + 2)/5) + (365*ySinceBC) + (ySinceBC/4) - (ySinceBC/100) + (ySinceBC/400) - 32045;
	
	if (hour >= 0 && hour < 12) {
        JDN += 1;
    }
    
    return JDN;
}