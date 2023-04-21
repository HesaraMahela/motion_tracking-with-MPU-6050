import numpy as np
import csv

from datetime import datetime






class Sensor():

    def __init__(self,_name,_serial):
        self.name = _name.encode('ascii')
        self.raw_data = np.zeros([3,3])
        self.calibrated_data = np.zeros([3,3])
        self.angles = np.zeros([3])
        self.serial = _serial
        self.accel_calibration_matrix = [np.zeros([3,3]), np.zeros(3)] # here all the data for the    for_all_three_parameters
        # is stored in a specific order to access
        self.gyro_calibration_matrix = [np.zeros([3, 3]), np.zeros(3)]
        self.magne_calibration_matrix = [np.zeros([3, 3]), np.zeros(3)]


        self.csv_name = str(datetime.now())
        with open(self.csv_name, 'a') as csvfile:
            # creating a csv writer object
            csvwriter = csv.writer(csvfile)
            # writing the fields
            #csvwriter.writerow(fields)


    def get_data(self):
        """ this function send the name of the sensors to collect the data and read the bytes """
        self.serial.write(self.name)
        line = self.serial.readline()  # read data until the end line character comes
        self.convert_data(line)

    def convert_data(self,line:str):

        data =[float(i) for i in line.split(',')] # split the serial reading with the ','
        if len(data) == 9:                        # check the data has numbers
            self.raw_data = np.array(data).reshape(3, 3) # set the readings to raw data format
        else:
            print('********** Wrong data type ***********')




    def calibrate(self):

        """ calibrated data value is replaced by this line """
        acc_calibrated_data = self.accel_calibration_matrix[0]*(self.raw_data[0] - self.accel_calibration_matrix[1])
        gyro_calibrated_data = self.gyro_calibration_matrix[0]*(self.raw_data[1] - self.gyro_calibration_matrix[1])
        magne_calibrated_data = self.magne_calibration_matrix[0]*(self.raw_data[2] - self.magne_calibration_matrix[1])
        self.calibrated_data = np.stack((acc_calibrated_data, gyro_calibrated_data, magne_calibrated_data))


    def roll_pitch_calculation(self):
        phi =np.arctan2([self.calibrated_data[0,1]] / [self.calibrated_data[0,1]])
        theta = np.arctan(self.calibrated_data[0,0]/(self.calibrated_data[0,1]*np.sin(phi) + self.calibrated_data[0,2]*np.cos(phi)))

        pass

    def accelerometer_calibration(self):
        pass

    def magnetometer_calibration(self):
        pass

    def write_data_to_csv(self,):

        with open(self.csv_name, 'a') as csvfile:
            # creating a csv writer object
            csvwriter = csv.writer(csvfile)

            # writing the fields
            # csvwriter.writerow(fields)






