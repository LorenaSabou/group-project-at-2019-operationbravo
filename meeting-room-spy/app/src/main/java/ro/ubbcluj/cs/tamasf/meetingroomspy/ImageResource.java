package ro.ubbcluj.cs.tamasf.meetingroomspy;

import org.json.JSONObject;
import org.restlet.data.MediaType;
import org.restlet.representation.Representation;
import org.restlet.representation.StringRepresentation;
import org.restlet.resource.Get;
import org.restlet.resource.ServerResource;

public class ImageResource extends ServerResource {
    @Get("json")
    public Representation getImage() {
        JSONObject result = new JSONObject();
        try {
            result.put("image", "Hello world");
        } catch (Exception e) {
            e.printStackTrace();
        }
        return new StringRepresentation(result.toString(), MediaType.APPLICATION_ALL_JSON);
    }
}
