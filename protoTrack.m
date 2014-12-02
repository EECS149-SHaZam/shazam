%% LED Configuration Parameters
m = 4;
k = 2;
l = m+k;
psi_tru = pi/6;

%% Create array of points
points(:,1) = [-10;10];
points(:,2) = points(:,1) + m*[cos(psi_tru); -sin(psi_tru)];
points(:,3) = points(:,2) + k*[cos(psi_tru); -sin(psi_tru)];

%% Generate camera measurements
theta1 = pi/2-atan2(points(2,1),points(1,1));
theta2 = pi/2-atan2(points(2,3),points(1,3));
theta3 = pi/2-atan2(points(2,2),points(1,2));

%% Calculate user position and orientation
c = (m/l) * (tan(theta2)-tan(theta1))/(tan(theta3)-tan(theta1));
a = 1-c;
b = tan(theta2) - tan(theta3)*c;

psi = atan2(-a,b);

v = l*(cos(psi)+sin(psi)*tan(theta2))/(tan(theta2) - tan(theta1));
u = v*tan(theta1);