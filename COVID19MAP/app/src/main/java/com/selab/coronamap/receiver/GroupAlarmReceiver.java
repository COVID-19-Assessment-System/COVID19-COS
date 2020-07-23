package com.selab.coronamap.receiver;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Build;

import com.selab.coronamap.service.GroupAlertService;

public class GroupAlarmReceiver extends BroadcastReceiver {

    @Override
    public void onReceive(Context context, Intent intent) {
        Intent i = null;
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O){
            i = new Intent(context, GroupAlertService.class);
            context.startForegroundService(i);
        }else{
            i = new Intent(context, GroupAlertService.class);
            context.startService(i);
        }
    }
}
