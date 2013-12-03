% rebase layout route_prefix=route
<div class="container">
  %if user is None:
  <h1>Login:</h1>
  <div class="panel panel-default">
    <div class="panel-body">
      <form role="form" action="/login" method="POST">
        <div class="form-group">
          <label for="user">Username:</label>
          <input type="user" class="form-control" id="user" placeholder="Enter username" name="user">
        </div>
        <div class="form-group">
          <label for="password">Password:</label>
          <input type="password" class="form-control" id="password" placeholder="Enter password" name="password">
        </div>
        <input class="btn btn-primary" type="submit" value="save" name="save">
      </form>
    </div>
  </div>
  %else:
  <h1>User: {{user}}</h1>
  %end
  <h1>Notes</h1>
  <div class="row">
    <div class="col-md-8">
      <table class="table table-condensed">
        <tr>
          <th>Id</th>
          <th>Title</th>
          <th>Note</th>
          <th>Action</th>
        </tr>
        %for row in rows:
        <tr>
          <td>{{row.get('id')}}</td>
          <td>{{row.get('title')}}</td>
          <td>{{row.get('content')}}</td>
          <td><form action="/delete/{{row.get('id')}}">
              <input class="btn btn-danger btn-xs" type="submit" value="Delete Note">
            </form>
          </td>
        </tr>
        %end
      </table>
    </div>
    <div class="col-md-4">
      <div class="panel panel-default">
        <div class="panel-body">
          <form role="form" action="/new" method="POST">
            <div class="form-group">
              <label for="title">Title:</label>
              <input type="title" class="form-control" id="title" placeholder="Enter title" name="title">
            </div>
            <div class="form-group">
              <label for="content">Note:</label>
              <input type="content" class="form-control" id="content" placeholder="Enter note" name="content">
            </div>
            <input class="btn btn-primary" type="submit" value="save" name="save">
          </form>
        </div>
      </div>
    </div>
  </div>
</div>
