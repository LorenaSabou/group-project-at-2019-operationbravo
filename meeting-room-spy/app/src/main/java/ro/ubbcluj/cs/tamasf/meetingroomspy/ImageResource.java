package ro.ubbcluj.cs.tamasf.meetingroomspy;

import android.media.Image;
import android.util.Log;

import org.json.JSONObject;
import org.restlet.data.MediaType;
import org.restlet.representation.Representation;
import org.restlet.representation.StringRepresentation;
import org.restlet.resource.Get;
import org.restlet.resource.ServerResource;

import java.util.Base64;

public class ImageResource extends ServerResource {
    private static final String TAG = ImageResource.class.getSimpleName();

    @Get("json")
    public Representation getImage() {
        JSONObject result = new JSONObject();

        try {
            byte[] imageBytes = ImageManager.getInstance().getImage();
            if(imageBytes != null) {
                String encoded = Base64.getEncoder().encodeToString(imageBytes);
                result.put("image", encoded);
            }
            else {
                result.put("image", "empty");
            }
        } catch (Exception e) {
            Log.e(TAG, e.getMessage());
        }

        return new StringRepresentation(result.toString(), MediaType.APPLICATION_ALL_JSON);
    }
}
