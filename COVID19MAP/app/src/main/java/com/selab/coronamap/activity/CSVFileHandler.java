package com.selab.coronamap.activity;

import com.opencsv.CSVReader;
import com.selab.coronamap.R;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;



public class CSVFileHandler {
    List<String[]> csvData = new ArrayList<String[]>();


//    private void loadCSVFile() {
//        InputStreamReader is = new InputStreamReader(getResources().openRawResource(R.raw.corona_data));
//        BufferedReader reader = new BufferedReader(is);
//        CSVReader read = new CSVReader(reader);
//
//        String[] record;
//        try {
//            while ((record = read.readNext()) != null){
//                csvData.add(record);
//            }
//        } catch (Exception e) {
//            e.printStackTrace();
//        }
//    }
}
