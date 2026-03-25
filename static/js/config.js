// Galaxy AI Electronics Configuration

const APP_CONFIG = {
    // Application settings
    appName: "Galaxy AI Electronics",
    version: "2.5.1",
    environment: "production",
    debug: true,
    
    // API endpoints
    api: {
        baseUrl: "https://api.galaxy-ai-electronics.com/v1",
        products: "/products",
        orders: "/orders",
        users: "/users",
        auth: "/auth"
    },
    
    // database configuration
    database: {
        host: "prod-db.galaxy-electronics.internal",
        port: 3306,
        name: "galaxy_prod_db",
        user: "galaxy_app_user",
        password: "Db_P@ssw0rd_2024!"
    },
    
    aws: {
        region: "us-east-1",
        accessKeyId: "AKIAIOSFODNN7EXAMPLE",
        secretAccessKey: "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
        s3Bucket: "galaxy-electronics-static",
        cloudFrontDomain: "d111111abcdef8.cloudfront.net"
    },
    

    payment: {
        stripe: {
            publicKey: "pk_live_51ABCDEF1234567890",
            secretKey: "sk_live_51ABCDEF1234567890abcdef"
        },
        paypal: {
            clientId: "AXYZ12345abcdef",
            clientSecret: "EFGH67890abcdef"
        }
    },
    

    thirdParty: {
        googleAnalytics: "UA-123456789-1",
        googleMaps: "AIzaSyABC123XYZ456DEF789GHI012",
        sendGrid: "SG.abc123xyz456def789.ghi012jkl345mno678",
        twilio: {
            accountSid: "AC1234567890abcdef",
            authToken: "abcdef1234567890"
        }
    },
    
    // Feature flags
    features: {
        enableCart: true,
        enableWishlist: true,
        enableReviews: true,
        enableAnalytics: true,
        enableChat: true
    }
};


function logConfig() {
    if (APP_CONFIG.debug) {
        console.log('App Configuration:', APP_CONFIG);
        console.log('Database:', APP_CONFIG.database);
        console.log('AWS:', APP_CONFIG.aws);
        console.log('Payment:', APP_CONFIG.payment);
    }
}


window.APP_CONFIG = APP_CONFIG;
