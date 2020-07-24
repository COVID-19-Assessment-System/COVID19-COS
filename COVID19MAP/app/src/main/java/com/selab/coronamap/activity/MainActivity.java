package com.selab.coronamap.activity;

import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.Window;
import android.widget.Button;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.FragmentActivity;

import com.aminyazdanpanah.maps.android.charts.ChartRenderer;
import com.aminyazdanpanah.maps.android.charts.PieChartRenderer;
import com.aminyazdanpanah.maps.android.charts.model.CMarker;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.LatLngBounds;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.iid.FirebaseInstanceId;
import com.google.firebase.iid.InstanceIdResult;
import com.google.maps.android.clustering.Cluster;
import com.google.maps.android.clustering.ClusterItem;
import com.google.maps.android.clustering.ClusterManager;
import com.opencsv.CSVReader;
import com.selab.coronamap.R;
import com.selab.coronamap.classes.CommHelper;
import com.selab.coronamap.service.GroupAlertService;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;

public class MainActivity extends FragmentActivity implements OnMapReadyCallback,
        ClusterManager.OnClusterClickListener<CMarker>,
        ClusterManager.OnClusterInfoWindowClickListener<CMarker>,
        ClusterManager.OnClusterItemClickListener<CMarker>,
        ClusterManager.OnClusterItemInfoWindowClickListener<CMarker> {
    private final static String TAG = "MainActivity";

    private GoogleMap googleMap;
    private GeocodeUtil geoutil;
    private ClusterManager<CMarker> clusterManager;
    private ChartRenderer chart;
    private String[] markerIcon = {"red", "green", "gray", "yellow", "blue", "black", "cyan", "white", "magenta"};
    private String[] names = {"1", "2", "3", "4", "5", "6", "7", "8", "9"};
    private int[] colors = {Color.RED, Color.GREEN, Color.GRAY, Color.YELLOW, Color.BLUE, Color.BLACK, Color.CYAN, Color.WHITE,Color.MAGENTA};
    private LatLngBounds location = new LatLngBounds(new LatLng(37.492332, 126.948789), new LatLng(37.502988, 126.983841));
    List<String[]> csvData = new ArrayList<>();


    private Intent grpAlertIntent;
    Button btnSignUp;
    FrameLayout layoutProgress;
    CommHelper commHelper;
    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        setContentView(R.layout.activity_main);
        commHelper = new CommHelper(getApplicationContext());
        geoutil = new GeocodeUtil(MainActivity.this);
        layoutProgress = findViewById(R.id.layout_progress);
        btnSignUp = findViewById(R.id.btn_signup);
        layoutProgress.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

            }
        });
        btnSignUp.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(MainActivity.this, SignupActivity.class);
                startActivity(intent);
            }
        });
        setUpMap();

        ((SupportMapFragment) getSupportFragmentManager().findFragmentById(R.id.map)).getMapAsync(this);
//        tempButtonToWatchData();
        loadCSVFile();  // load corona19 data

        if(GroupAlertService.serviceIntent == null){        // Code for connecting local notification service
            grpAlertIntent = new Intent(this, GroupAlertService.class);
            startService(grpAlertIntent);   // To start the service
        }else{
            grpAlertIntent = GroupAlertService.serviceIntent;
        }

        // Code to get firebase instance id. the id is applied to distinguish devices.
        FirebaseInstanceId.getInstance().getInstanceId().addOnCompleteListener(new OnCompleteListener<InstanceIdResult>() {
            @Override
            public void onComplete(@NonNull Task<InstanceIdResult> task) {
                if (!task.isSuccessful()){
                    return;
                }
                String token = task.getResult().getToken();     // To get current device's id

                Log.d(TAG, token);
//                Toast.makeText(MainActivity.this, token, Toast.LENGTH_SHORT).show();
            }
        });
    }

    private LatLng addressToCoords(String address){
        ArrayList<GeocodeUtil.GeoLocation> locationList = geoutil.getGeoLocationListUsingAddress(address);
        return new LatLng(locationList.get(0).latitude, locationList.get(0).longitude);
    }

    private void loadCSVFile() {

        InputStreamReader is = new InputStreamReader(getResources().openRawResource(R.raw.corona_data));
        BufferedReader reader = new BufferedReader(is);
        CSVReader read = new CSVReader(reader);

        String[] record;
        try {
            while ((record = read.readNext()) != null){
                csvData.add(record);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
//        for(String[] strArray: csvData) {
//            System.out.println(Arrays.toString(strArray));
//        }
    }

    @Override
    protected void onResume() {
        super.onResume();
    }

    private void setUpMap() {
        Log.d(TAG, "SetupMap");
    }

    @Override
    public void onMapReady(GoogleMap map) {
        Log.d(TAG, "OnMapReady");
        if (googleMap != null) {
            return;
        }
        this.googleMap = map;
        demo();
        addItems();
        clusterManager.cluster();

    }

    @Override
    public boolean onClusterClick(Cluster<CMarker> cluster) {
        LatLngBounds.Builder builder = LatLngBounds.builder();
        for (ClusterItem item : cluster.getItems()) {
            builder.include(item.getPosition());
        }

        final LatLngBounds bounds = builder.build();

        try {
            googleMap.animateCamera(CameraUpdateFactory.newLatLngBounds(bounds, 100));
        } catch (Exception e) {
            e.printStackTrace();
        }

        return true;
    }

    @Override
    public void onClusterInfoWindowClick(Cluster<CMarker> cluster)  {
        getLayoutInflater();
    }

    @Override
    public boolean onClusterItemClick(CMarker cMarker) {
        return false;
    }

    @Override
    public void onClusterItemInfoWindowClick(CMarker cMarker) {

    }

    private void demo() {
        googleMap.setOnMapLoadedCallback(new GoogleMap.OnMapLoadedCallback() {
            @Override
            public void onMapLoaded() {
                googleMap.animateCamera(CameraUpdateFactory.newLatLngBounds(location, 0));
            }
        });

        clusterManager = new ClusterManager<>(this, googleMap);

        chart = new PieChartRenderer(getApplicationContext(), googleMap, clusterManager);
        chart.colors(colors);
        chart.names(names);
        clusterManager.setRenderer(chart);

        googleMap.setOnCameraIdleListener(clusterManager);
        googleMap.setOnMarkerClickListener(clusterManager);
        googleMap.setOnInfoWindowClickListener(clusterManager);
        clusterManager.setOnClusterClickListener(this);
        clusterManager.setOnClusterInfoWindowClickListener(this);
        clusterManager.setOnClusterItemClickListener(this);
        clusterManager.setOnClusterItemInfoWindowClickListener(this);

    }

    private void addItems() {
        Log.d(TAG, "addItems");
        new Thread(new Runnable() {
            @Override
            public void run() {
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    HashSet<String> idset = new HashSet<>();
                    for (String[] strArray: csvData) {
                        try{
                            int clusterId = Integer.parseInt(strArray[7]);
                            idset.add(strArray[7]);
                            CMarker marker = new CMarker(addressToCoords(strArray[3]), String.valueOf(clusterId+1), getDrawableId(markerIcon[clusterId]));
                            marker.setTitle(String.valueOf(clusterId+1));

                            clusterManager.addItem(marker);
                        }catch (Exception e){}
                    }
                    Log.d(TAG, idset.toString());
                    LinearLayout layoutLegend = findViewById(R.id.layout_legend);
                    for(int i = idset.size()-1; i >= 0;i--){
                        Log.d(TAG, String.valueOf(i));

                        LayoutInflater vi = (LayoutInflater) getApplicationContext().getSystemService(Context.LAYOUT_INFLATER_SERVICE);
                        View v = vi.inflate(R.layout.view_legende, null);

                        View vColor = v.findViewById(R.id.legend_color);
                        vColor.setBackgroundColor(colors[i]);
                        TextView vName = v.findViewById(R.id.legend_name);
                        vName.setText(String.valueOf(i));

                        layoutLegend.addView(v, 0, new ViewGroup.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT));
                    }
                    layoutProgress.setVisibility(View.GONE);
                }
            });
            }
        }).start();

    }
    private int getDrawableId(String name) {
        Log.d(TAG, "getDrawableId");

        try {
            Field field = R.drawable.class.getField("marker_" + name);
            return field.getInt(null);
        } catch (Exception e) {
            //
        }
        return -1;
    }

    public void pieChart(View v) {
        location = new LatLngBounds(
//                new LatLng(35.607781, 51.187924), new LatLng(35.778940, 51.548771));
                new LatLng(37.492332, 126.948789), new LatLng(37.502988, 126.983841));
        resetMap();
    }

    private void resetMap() {
        Log.d(TAG, "resetMap");
        clusterManager.clearItems();
        googleMap.clear();
        demo();
        addItems();
        clusterManager.cluster();
    }
}
