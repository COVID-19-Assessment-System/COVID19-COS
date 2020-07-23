package com.selab.coronamap.activity;

import android.graphics.Color;
import android.os.Bundle;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.TextView;

import androidx.annotation.Nullable;
import androidx.fragment.app.FragmentActivity;

import com.aminyazdanpanah.maps.android.charts.BarChartRenderer;
import com.aminyazdanpanah.maps.android.charts.ChartRenderer;
import com.aminyazdanpanah.maps.android.charts.DonutChartRenderer;
import com.aminyazdanpanah.maps.android.charts.PieChartRenderer;
import com.aminyazdanpanah.maps.android.charts.model.CMarker;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.LatLngBounds;
import com.google.maps.android.clustering.Cluster;
import com.google.maps.android.clustering.ClusterItem;
import com.google.maps.android.clustering.ClusterManager;
import com.selab.coronamap.R;

import java.lang.reflect.Field;
import java.util.Random;

public class MainActivity extends FragmentActivity implements OnMapReadyCallback,
        ClusterManager.OnClusterClickListener<CMarker>,
        ClusterManager.OnClusterInfoWindowClickListener<CMarker>,
        ClusterManager.OnClusterItemClickListener<CMarker>,
        ClusterManager.OnClusterItemInfoWindowClickListener<CMarker> {
    private GoogleMap googleMap;

    private ClusterManager<CMarker> clusterManager;
    private Random mRandom = new Random(1984);
    private Random r = new Random();
    private ChartRenderer chart;
    private String[] names = {"Toyota", "Ford", "Honda", "Dodge"};
    private String[] markerIcon = {"red", "green", "blue", "yellow"};
    private int[] colors = {Color.RED, Color.GREEN, Color.BLUE, Color.YELLOW};
    private boolean pieChart = true;
    private boolean barChart, donutChart;
    private LatLngBounds location = new LatLngBounds(
            new LatLng(37.492332, 126.948789), new LatLng(37.502988, 126.983841));
    private Button btnPie, btnDonut, btnBar;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        this.getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN,
                WindowManager.LayoutParams.FLAG_FULLSCREEN);
        setContentView(R.layout.activity_main);
        setUpMap();

        btnPie = findViewById(R.id.btn_pie);
        btnBar = findViewById(R.id.btn_bar);
        btnDonut = findViewById(R.id.btn_donut);
        btnPie.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                pieChart(view);
            }
        });

        btnBar.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                barChart(view);
            }
        });

        btnDonut.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                donutChart(view);
            }
        });
    }

    @Override
    protected void onResume() {
        super.onResume();
        setUpMap();
    }

    private void setUpMap() {
        ((SupportMapFragment) getSupportFragmentManager().findFragmentById(R.id.map)).getMapAsync(this);
    }

    @Override
    public void onMapReady(GoogleMap map) {
        if (googleMap != null) {
            return;
        }
        this.googleMap = map;
        demo();

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

        if (pieChart) {
            chart = new PieChartRenderer(getApplicationContext(), googleMap, clusterManager);
        } else if (barChart) {
            chart = new BarChartRenderer(getApplicationContext(), googleMap, clusterManager);
        } else if (donutChart) {
            chart = new DonutChartRenderer(getApplicationContext(), googleMap, clusterManager);
        }
        chart.colors(colors);
        chart.names(names);
        clusterManager.setRenderer(chart);

        setTexts();

        getLayoutInflater();
        googleMap.setOnCameraIdleListener(clusterManager);
        googleMap.setOnMarkerClickListener(clusterManager);
        googleMap.setOnInfoWindowClickListener(clusterManager);
        clusterManager.setOnClusterClickListener(this);
        clusterManager.setOnClusterInfoWindowClickListener(this);
        clusterManager.setOnClusterItemClickListener(this);
        clusterManager.setOnClusterItemInfoWindowClickListener(this);
        addItems();
        clusterManager.cluster();
    }

    private void setTexts() {
        TextView red = findViewById(R.id.red);
        TextView green = findViewById(R.id.green);
        TextView blue = findViewById(R.id.blue);
        TextView yellow = findViewById(R.id.yellow);

        red.setText(names[0]);
        green.setText(names[1]);
        blue.setText(names[2]);
        yellow.setText(names[3]);
    }


    private void addItems() {
        for (int i = 0; i < 300; i++) {
            int rand = r.nextInt(4);

            CMarker marker = new CMarker(randomPosition(), names[rand], getDrawableId(markerIcon[rand]));
            marker.setTitle(names[rand]);

            clusterManager.addItem(marker);
        }
    }
    private int getDrawableId(String name) {
        try {
            Field field = R.drawable.class.getField("marker_" + name);
            return field.getInt(null);
        } catch (Exception e) {
            //
        }
        return -1;
    }

    private LatLng randomPosition() {
        double minLatitude = location.southwest.latitude;
        double maxLatitude = location.northeast.latitude;
        double minLongitude = location.southwest.longitude;
        double maxLongitude = location.northeast.longitude;
        return new LatLng(
                minLatitude + (maxLatitude - minLatitude) * mRandom.nextDouble(),
                minLongitude + (maxLongitude - minLongitude) * mRandom.nextDouble());
    }

    public void pieChart(View v) {
        pieChart = true;
        location = new LatLngBounds(
//                new LatLng(35.607781, 51.187924), new LatLng(35.778940, 51.548771));
                new LatLng(37.492332, 126.948789), new LatLng(37.502988, 126.983841));

        names = new String[]{"Hyundai", "Kia", "Samsung", "SSangYong"};
        resetMap();
    }

    public void barChart(View v) {
        donutChart = pieChart = false;
        barChart = true;
        location = new LatLngBounds(
                new LatLng(29.504185, 52.423688), new LatLng(29.699397, 52.650020));
        names = new String[]{" <$1000 ", "$1000 - $2000", "$2000 - $3000", "> $3000"};
        resetMap();
    }

    public void donutChart(View v) {
        barChart = pieChart = false;
        donutChart = true;
        location = new LatLngBounds(
                new LatLng(38.022076, 46.224534), new LatLng(38.119992, 46.377530));
        names = new String[]{"School", "Hospital", "Police Station", "Market"};
        resetMap();
    }

    private void resetMap() {
        clusterManager.clearItems();
        googleMap.clear();
        demo();
    }
}
