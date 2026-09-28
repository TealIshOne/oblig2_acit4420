# OPTION A | Smart Fitness Session Analyze

obligatory assignment

| Student name                      | Student number | Course             |
| --------------------------------- | -------------- | ------------------ |
| ~~Ida Cecilie Brænde Svendsen~~ | s371425        | ACIT4420 - oblig 1 |

## Short project description

This code simulates an application that processes and analyses singular or multi session bio-metric

signal data (heart rate, skin response, body temperature, activity level and signal quality).

The intnetion of the aplication is to validate incoming date, filter corrupt observation, throught the validated data

The program classifies the session type, detects recovery period, counts valid/invalid data sets and data entries.

The main outputs to concider is a human readable printout of relevant data, alongside a summary dictionary of the same data

## Class design and explanation of each class's responsibility (OOC architechture

## Assumptions and classification rules

The code is based on a two tiere classification aproach, first through data comparison to baseline thresholds, then determining overall session tyoe via majority voting and trend detection.

1. Metric-level classification rules:
   1. Resting: hr<=baselineHR +10BPM
   2. Moderate act: baselineHR +10BPM < hr <baselineHR +30BPM
   3. High act: baselineHR +30BPM < hr <220   //a value taken from rule that max heart rate should be 220 -your age, this account for slight signal missalignment but is still sensibly restricted
   4. Inconclusive: signal quality <0.5, or missing data
2. Classification and priority rules:
   1. Bad/Corrupted data: if signal quality is to low  or valid observations reach zero the session is qualified as `"session type inconclusive due to missing / bad data"`
   2. Recovery override rule: if recoverytracker() detects downwards trend i.e. recovery session, the data is omitted to avoid data "polution", the recovery max level will in some instances get the session flagged as high activety. if all datasets are recovery the  math functions default to raw valid data.
   3. Majority counting rule, will in cases of no recovery default to a "majority type" rule, when counting majority the, if there are two of the same classifications, e.g. rest +rest + mod + mod, will default to rest classification as it is the first instance met in the if else statments that determines classification
   4. Tie-breaker: if the session types are equal, the session may be labled "inconclusive or unknown sessiontype"

## Stated assumptions:

1. Baseline accuracy: the provided datagenerator is assumed to be accurate in its data generation, although the temperature does seems low
2. The  timing of  datasets passed to sessionMath is assumed to be of no importance as there is no timing concernes or handeling in the code
3. Data scope:  summary metrics (min, max, avg) are calculated across valid and usable observations combined. unusable or corrupted data is omitted in these calculations to prevent skewage
4. When low activety and high activety data sessions are entered together the session returned is the average of the sessions across al sessions,

### *Participant*

| Role                                                                   | Key responsibilities                                                                                                                                                                                                        |
| ---------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| modesl participant profile information and baseline biometric-signals  | encapsulates participant identifiers (`ID`) and baseline metrics/vitals (`Baseline_HR`, `Baseline_Skin`, `Baseline_Temp` )Provides the @classmethod method `instantiate_profile()` to build participant object.  |

### *Observation*

| Role                                                                         | Key Responsibilities                                                                                                                                                                                                                  |
| ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| validates, cleans and allocate valid data by`ValidDataContainerAllocation` | checks raw data enteries for corrupt/low signal data types, missing keys or out of bound values.<br />seperates rawinput into valid, and invalid containers.<br />allocates clean metricks.<br />verifys data type for further work. |

### *SessionsStorage*

| Role                           | Key Responsibilities                                                                                                                                                                                                            |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| manage multi- session datasets | holds collections of raw session data across multiple sessions.<br />batch vallidates  through compositionof `ValidateAll()`.<br />track global counts of usable vs unusable observations and valid vs invalid sesion count |

### *sessionMath*

| Role                                                                                                      | Key Responsibilities                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| --------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| executes calculations using standard Python math functions. tracks downward trends, and session raporting | uses composition to store`Participant` to store refference baselines. for comparisons.<br />overides `ValidateAll()` after inheritance, to extend storage validation by extracting metric lists.<br />calculates max, avg, min, and provides range summary statistics for each vital metric (`hr_info`, `sr_info`, `temp_i`, `al_i`, `signal_info`).<br />wvaluate  recovery presence in datasets.<br />classify activety classess.<br />generate human readable console raport, and structured summary dictionary<br />  |

## Instructions to install and run the code

**Prerequisits**:

* Python 3.14
* no external third-party dependencies  required (built using standard Python lib)

**How to run:**

git clone https://github.com/TealIshOne/Oblig1_acit4420.git
  cd Oblig1_acit4420

python3 main.py

python3 tests.py

## Example output

### Summary of tested scenarios

the test.py script automaticly evaluates the following sections in order:

1. Testing of individual classes with single dataset input (evenwhen more is possible)
2. 5 required scenarios
   1. scenario: resting session: evaluares low-intensity data against baseline vitals
   2. scenario: moderate activity: evaluates moderate heartrate and activety metrics against
   3. scenario: high activity:
   4. scenario: recovery session: evaluates downwards trend within session, and removal of such values so they do not polute math calculations
   5. scenario: poor quality,  evaluates ystem resilience to poor signal quality, type changes
3. additional functionalities (mixed signal innput): evaluates multi-session-type combinations (e.g. resting +high ) and malformed data arrays

code print snippit:


--- Case 4: High Activity + High Activity + Recovery ---
Result: Classified as 'high activity' | Recovery detected: True

---

you just finished a session of high activity
great!

---

your maximum values across the sessions were:
your heart rate reached................................ 150 BPM
your skin respone reached.............................. 2.11
your temperature rate reached.......................... 32.94 C
your activety level reached............................ 0.92

---

your average values across the sessions were:
your heart rate averaged............................... 133.1 BPM
your skin respone averaged............................. 1.81
your temperature averaged.............................. 32.5 C
your acticity level averaged........................... 0.74

---

your minimum values across the sessions were:
your heart rate hit.................................... 87 BPM
your skin respone hit.................................. 1.42
your temperature hit................................... 31.87 C
your activity level hit................................ 0.12

---

your ranges were as follows
your heart rate spanned................................ 63 BPM
your skin respone spanned.............................. 0.69
your temperature spanned............................... 0.63 C
your acticety level spanned............................ 0.8

---

recovery period?....................................... yes
invalid data count?.................................... 0
valid data count?...................................... 36

---

[Structured Dictionary Output]:
{'HEARTRATE': {'reference': 73, 'max': 150, 'avg': 133.1, 'min': 87}, 'SKINRESPONSE': {'reference': 2.28, 'max': 2.11, 'avg': 1.81, 'min': 1.42}, 'TEMPERATURE': {'reference': 32.12, 'max': 32.94, 'avg': 32.5, 'min': 31.87}, 'ACTIVITY': {'reference': 'NA', 'max': 0.92, 'avg': 0.74, 'min': 0.12}, 'RECOVERY': True, 'ACTIVETY TYPE': 'high activity', 'DATASET w/INVALID DATA': 0, 'DATASET w/VALID DATA': 3, 'INVALIDCOUNT': 0, 'VALIDCOUNT': 36}


## Known limitations

* **Recovery Baseline Fallback**: if all dataset sessions entered are recovery,
  stats fall back to being derived from raw data. This is to avoid returning 0
  when recovery values are removed to not polute min, max, avg values. 0 value
  allocation is reserved to 'bad data' entries
* **Threshold boundaries:** session classification is reliant on fixed offsets boundaries,
  these may not be accurate and are not personalied to different personal thresholds
  that may differe between participants
* **Recovery removal:** recovery values are removed from datasets so they do not polute calculations
  and classification efforts.this is because these functions are based on threshold values. and the
  high to low nature of recovery caused issues with  classification  and was labled as high activety
  due to the way the code was designed.
* **Joint data classification**: when multiple session data sets is used, the code runs math across the joint dataset and not individually for classification purposes. this means that when e.g. resting + resting + highactivity + high activity, data sets are entered the code will classify this joint session as moderate, and will not return the  dataset as inconclusive
