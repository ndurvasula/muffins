#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>


//struct encapsulating split based on theorem 2.8
struct MuffinSplit {

    int foundSplit;

    int m;
    int s;

    int x1;
    int x2;

    int y1;
    int y2;

    int z1;
    int z2;

    int deltNum;
    int deltDenom;
    int specialCase;
};

//this stuff should be mostly self-explanatory. since we want to
//stuff to be as pretty as possible, keep the delta as a fraction
//and use these helpfer functions. note, I feel like it might be
//easeier if we have both this format and the raw delta- i'm pretty
//sure that C's floats compares using delta-approximate equality

//also, we should prob move this to its own module, but that would make
//emailing it harder :/
//TODO: INSTALL GIT DUDE
struct Fraction {
    int num;
    int denom;
};

struct Fraction fractionMin(struct Fraction a, struct Fraction b) {
    float aVal = ((float) a.num)/a.denom;
    float bVal = ((float) b.num)/b.denom;

    if(aVal < bVal) {
        return a;
    }

    return b;
}

struct Fraction fractionMax(struct Fraction a, struct Fraction b) {
    float aVal = ((float) a.num)/a.denom;
    float bVal = ((float) b.num)/b.denom;

    if(aVal > bVal) {
        return a;
    }

    return b;
}

struct Fraction fractionSimplify(struct Fraction a) {
    int i;

    for(i = a.denom; i > 1; i--) {
        if(a.num % i == 0 && a.denom % i == 0) {
            a.num /= i;
            a.denom /= i;

            return a;
        }
    }

    return a;
}

bool fractionEqual(struct Fraction a, struct Fraction b) {
    a = fractionSimplify(a);
    b = fractionSimplify(b);

    return a.num == b.num && a.denom == b.denom;
}

struct Fraction fractionAdd(struct Fraction a, struct Fraction b) {
    a = fractionSimplify(a);
    b = fractionSimplify(b);

    int num = (a.num * b.denom) + (a.denom * b.num);
    int denom = a.denom * b.denom;

    struct Fraction result = {num, denom};

    return fractionSimplify(result);
}

float fracToVal(struct Fraction a) {
    return ((float) a.num)/((float)a.denom);
}

//so the general formula fails under 1/3. this is a prelim calculation
//of the delta using thm 2.4, I'm pretty sure there's an easier way of
//coding this using just {} since c's structs work like that, but who knows
struct Fraction calcSmallDeltaUB(int m, int s) {

    struct Fraction caseOne = {m, 3*s};

    float thingOne = ((float) m)/(2*(s-m));
    struct Fraction caseTwoA = {m, s};
    struct Fraction caseTwoB = {s-m, s*ceil(thingOne)};
    struct Fraction caseTwoC = {m*ceil(thingOne) - s + m, s*ceil(thingOne)};
    struct Fraction caseTwo = fractionMin(caseTwoA, fractionMin(caseTwoB, caseTwoC));

    struct Fraction caseThreeA = {m, s};
    struct Fraction caseThreeB = {s-m, s*floor(thingOne)};
    struct Fraction caseThreeC = {m*floor(thingOne) - s + m, s*floor(thingOne)};
    struct Fraction caseThree = fractionMin(caseThreeA, fractionMin(caseThreeB, caseThreeC));

    float thingTwo = ((float)2*s)/m;
    struct Fraction caseFourA = {1, ceil(thingTwo)};
    struct Fraction caseFourB = {m*ceil(thingTwo)-s, s*ceil(thingTwo)};
    struct Fraction caseFourC = {m, 2*s};
    struct Fraction caseFour = fractionMin(caseFourA, fractionMin(caseFourB, caseFourC));

    struct Fraction caseFiveA = {1, floor(thingTwo)};
    struct Fraction caseFiveB = {m*floor(thingTwo) - s, s*floor(thingTwo)};
    struct Fraction caseFiveC = {m, 2*s};
    struct Fraction caseFive = fractionMin(caseFiveA, fractionMin(caseFiveB, caseFiveC));

    return fractionMax(caseOne, fractionMax(caseTwo, fractionMax(caseThree, fractionMax(caseFour, caseFive))));
}

struct Fraction calcSmallDeltaLB(int m, int s, int * minX, int * minY) {
    int x, y, a;
    struct Fraction maxPart = {0, 1};

    for(x = 1; x < s; x++) {
        for(y = 1; y < s; y++) {
            if(x*y > s || (x*y) % (m-y) != 0) {
                continue;
            }

            for(a = 1; a <= (m-y); a++) {
                if((a*(s - x*y)) % (m-y) == 0) {
                    break;
                }
            }

            struct Fraction partOne = {1, x};
            struct Fraction partTwo = {m*x - s, s*x};
            struct Fraction partThree = {m, a*s};
            struct Fraction minPart = fractionMin(partOne, fractionMin(partTwo, partThree));

            if(!fractionEqual(maxPart, fractionMax(minPart, maxPart))) {
                maxPart = fractionMax(minPart, maxPart);
                *minX = x;
                *minY = y;
            }
        }
    }

    return maxPart;
}

//figure stuff out using our paper
int gasarchSplit(int m, int s, struct MuffinSplit *gSplit) {
    gSplit->m = m;
    gSplit->s = s;
    gSplit->foundSplit = 0;
    gSplit->specialCase = 0;

    //special case that muffins divides students, our delt is going to
    //be 1, set special case (for printing), and return noting that we
    //found a split
    if(m % s == 0) {
        gSplit->deltNum = 1;
        gSplit->deltDenom = 1;
        gSplit->foundSplit = 1;
        gSplit->specialCase = 1;

        return 0;
    }

    //thm 2.1.2
    if(s % (2*m) == 0) {

        gSplit->deltNum = 1;
        gSplit->deltDenom = 2;
        gSplit->foundSplit = 1;
        gSplit->specialCase = 1;

        return 0;

    }

    //thm 2.1.4-5
    if(m == 1 || m == 2 && s % 2 == 1) {
        gSplit->deltNum = 1;
        gSplit->deltDenom = s;
        gSplit->foundSplit = 1;
        gSplit->specialCase = 1;

        return 0;
    }

    double fracPart = 2*((float)m)/s;

    //deltas based on 2.2.2
    struct Fraction delt1 = {m, (s*ceil(fracPart))};
    struct Fraction delt2 = {(s * floor(fracPart))-m, (s * floor(fracPart))};

    //calc UB for small m/s
    struct Fraction smallDeltUB = calcSmallDeltaUB(m, s);

    //calc LB for small m/s
    int x, y;
    struct Fraction smallDeltLB = calcSmallDeltaLB(m, s, &x, &y);

    
    struct Fraction minDelt = fractionMin(delt1, delt2);

    //if small delta is less than 1/3, use it else keep delta from 2.2.2
    if (fracToVal(smallDelt) < .33333) {
        minDelt = smallDelt;
    }

    minDelt = fractionSimplify(minDelt);

    //try theorem 2.8
    int x1, x2, y1, y2, z1, z2;

    //search over all x1, x2, z1, z2
    for(x1 = 1; x1 < s; x1++) {
        x2 = s - x1;

        for(z1 = 0; z1 < 2*m; z1++) {
            for(z2 = 0; z2 < 2*m; z2++) {

                //basically use 2.8.3 to calculate y1,y2 ensuring that they are
                //natural numbers greater than 0
                if((2*m - z1*x1 - z2*x2) % x1 != 0 || (2*m - z1*x1 - z2*x2) < 0) {
                    continue;
                } else {
                    y1 = (2*m - z1*x1 - z2*x2) / (2*x1);
                }

                if((2*m - z1*x1 - z2*x2) % x2 != 0  || (2*m - z1*x1 - z2*x2) < 0) {
                    continue;
                } else {
                    y2 = (2*m - z1*x1 - z2*x2) / (2*x2);
                }

                //ensure y's from 2.8.3 are same as 2.8.4-5
                struct Fraction y1Delt = {minDelt.num*y1, minDelt.denom};
                struct Fraction z1Over2 = {z1, 2};
                struct Fraction mOverS = {m, s};

                struct Fraction y2Delt = {(minDelt.denom - minDelt.num)*y2, minDelt.denom};
                struct Fraction z2Over2 = {z2, 2};

                if(fractionEqual(fractionAdd(y1Delt, z1Over2), mOverS)
                    && fractionEqual(fractionAdd(y2Delt, z2Over2), mOverS)) {
                        gSplit->deltNum = minDelt.num;
                        gSplit->deltDenom = minDelt.denom;
                        gSplit->x1 = x1;
                        gSplit->x2 = x2;
                        gSplit->y1 = y1;
                        gSplit->y2 = y2;
                        gSplit->z1 = z1;
                        gSplit->z2 = z2;
                        gSplit->foundSplit = 1;

                        return 0;
                    }
            }
        }
    }

    //try same thing using 1 - delta
    minDelt.num = minDelt.denom - minDelt.num;

    for(x1 = 1; x1 < s; x1++) {
        x2 = s - x1;

        for(z1 = 0; z1 < 2*m; z1++) {
            for(z2 = 0; z2 < 2*m; z2++) {

                if((2*m - z1*x1 - z2*x2) % x1 != 0 || (2*m - z1*x1 - z2*x2) < 0) {
                    continue;
                } else {
                    y1 = (2*m - z1*x1 - z2*x2) / x1;
                }

                if((2*m - z1*x1 - z2*x2) % x2 != 0  || (2*m - z1*x1 - z2*x2) < 0) {
                    continue;
                } else {
                    y2 = (2*m - z1*x1 - z2*x2) / x2;
                }

                struct Fraction y1Delt = {minDelt.num*y1, minDelt.denom};
                struct Fraction z1Over2 = {z1, 2};
                struct Fraction mOverS = {m, s};

                struct Fraction y2Delt = {(minDelt.denom - minDelt.num)*y2, minDelt.denom};
                struct Fraction z2Over2 = {z2, 2};

                if(fractionEqual(fractionAdd(y1Delt, z1Over2), mOverS)
                    && fractionEqual(fractionAdd(y2Delt, z2Over2), mOverS)) {
                        gSplit->deltNum = minDelt.num;
                        gSplit->deltDenom = minDelt.denom;
                        gSplit->x1 = x1;
                        gSplit->x2 = x2;
                        gSplit->y1 = y1;
                        gSplit->y2 = y2;
                        gSplit->z1 = z1;
                        gSplit->z2 = z2;
                        gSplit->foundSplit = 1;

                        return 0;
                    }
            }
        }
    }


    //no match found
    //revert delta
    gSplit->deltNum = minDelt.denom - minDelt.num;
    gSplit->deltDenom = minDelt.denom;
    return -1;
}

//print split based on paper
void printSplit(struct MuffinSplit mSplit) {


    //warn for small deltas
    if(((float)mSplit.deltNum)/mSplit.deltDenom < .33333 && mSplit.deltNum > 0) {
        printf("(caution: delta less than 1/3) ");
    }

    printf("m: %d, modulo: %d, s: %d, ", mSplit.m, mSplit.m % mSplit.s, mSplit.s);
    if(mSplit.foundSplit == 0 ) {
        printf("no possible combination found, delta:%d/%d\n", mSplit.deltNum, mSplit.deltDenom);
    } else if(mSplit.specialCase == 1) {
        printf("delta: %d/%d\n", mSplit.deltNum, mSplit.deltDenom);
    } else {
        printf("x1: %d, x2: %d, y1: %d, y2: %d, z1: %d, z2: %d, delta: %d/%d\n", mSplit.x1, mSplit.x2, mSplit.y1, mSplit.y2, mSplit.z1, mSplit.z2, mSplit.deltNum, mSplit.deltDenom);
    }
}

//calculate and print split based on our paper
int calcAndPrintSplit(int m, int s) {
    struct MuffinSplit gSplit;
    int status = gasarchSplit(m, s, &gSplit);

    printSplit(gSplit);
}

//print all cases from 1 to s*50
int printAllCases(int s) {
    struct MuffinSplit gSplit;

    int m;
    for(m = 1; m < s*50; m++) {
        int status = gasarchSplit(m, s, &gSplit);

        printSplit(gSplit);

    }
}

//only print failed cases
int printFailModulos(int s) {
    struct MuffinSplit gSplit;

    int m;
    for(m = s; m < s*50; m++) {
        int status = gasarchSplit(m, s, &gSplit);

        if (status == -1) {
            printSplit(gSplit);
        }

    }
}

int main(int argc, char *argv[]) {

    //c's first arg is the prog name
    if(argc != 3) {

        printf("wrong number of arguments\n");
        return -1;
    }
    //you could def override this to take variable # of args

    //read args as ints
    int m = atoi(argv[1]);
    int s = atoi(argv[2]);


    calcAndPrintSplit(m,s);// prints for one case
    //printAllCases(s); //prints for m= 1 - s*50 cases

    //printFailModulos(s);
}
