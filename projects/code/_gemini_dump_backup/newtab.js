// Method 3: Pass data to iframe via URL parameters
document.addEventListener('DOMContentLoaded', function() {
    const iframe = document.getElementById('mainFrame');
    
    // Collect extension data to pass to the iframe
    const extensionData = {
        source: 'extension',
        version: '11.0',
        timestamp: Date.now(),
        userAgent: navigator.userAgent,
        language: navigator.language,
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        screenWidth: screen.width,
        screenHeight: screen.height,
        extensionId: chrome?.runtime?.id || 'unknown'
    };
    
    // Try to get data from Chrome storage if available
    if (typeof chrome !== 'undefined' && chrome.storage) {
        chrome.storage.local.get(['extensionData', 'userPreferences', 'lastActivity', 'iid'], function(result) {
            // Merge stored data with extension data
            const combinedData = {
                ...extensionData,
                storedData: result.extensionData || null,
                preferences: result.userPreferences || null,
                lastActivity: result.lastActivity || null,
                iid: result.iid || null
            };
            
            // Create URL parameters
            const params = new URLSearchParams({
                source: combinedData.source,
                version: combinedData.version,
                timestamp: combinedData.timestamp.toString(),
                lang: combinedData.language,
                tz: combinedData.timezone,
                screen: `${combinedData.screenWidth}x${combinedData.screenHeight}`,
                ext_id: combinedData.extensionId,
                data: JSON.stringify({
                    stored: combinedData.storedData,
                    prefs: combinedData.preferences,
                    activity: combinedData.lastActivity
                })
            });
            
            // Add iid parameter if it exists
            if (combinedData.iid) {
                params.set('iid', combinedData.iid);
            }
            
            // Update iframe source with parameters
            iframe.src = `https://savvyfinder.com/newtab?${params.toString()}`;
        });
    } else {
        // Fallback if Chrome APIs are not available
        const params = new URLSearchParams({
            source: extensionData.source,
            version: extensionData.version,
            timestamp: extensionData.timestamp.toString(),
            lang: extensionData.language,
            tz: extensionData.timezone,
            screen: `${extensionData.screenWidth}x${extensionData.screenHeight}`,
            ext_id: extensionData.extensionId
        });
        
        iframe.src = `https://savvyfinder.com/newtab?${params.toString()}`;
    }
    
    // Listen for storage changes and update iframe if needed
    if (typeof chrome !== 'undefined' && chrome.storage) {
        chrome.storage.onChanged.addListener(function(changes, namespace) {
            if (changes.extensionData || changes.userPreferences) {
                // Reload iframe with updated data
                console.log('Extension data updated, refreshing iframe...');
                location.reload();
            }
        });
    }

});
